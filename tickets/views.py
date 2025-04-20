from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Ticket, Department, TicketStatus, TicketPriority, TicketMessage, TicketAttachment
from accounts.models import Profile
from django.core.paginator import Paginator
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.db.models import Max, OuterRef, Subquery


def get_pages_to_show(current_page, total_pages):
    if total_pages <= 3:
        return list(range(1, total_pages + 1))

    if current_page <= 2:
        return [1, 2, 3, '...', total_pages]

    if current_page >= total_pages - 1:
        return [1, '...', total_pages - 2, total_pages - 1, total_pages]

    return [1, '...', current_page - 1, current_page, current_page + 1, '...', total_pages]


@login_required
def dashboard(request):
    ticket_stats = {
        'new': Ticket.objects.filter(user=request.user, status__name='جدید').count(),
        'in_progress': Ticket.objects.filter(user=request.user, status__name='در حال بررسی').count(),
        'answered': Ticket.objects.filter(user=request.user, status__name='پاسخ داده شده').count(),
        'closed': Ticket.objects.filter(user=request.user, status__name='بسته شده').count(),
    }
    profile = Profile.objects.get(user=request.user)

    last_message_subquery = TicketMessage.objects.filter(ticket=OuterRef('pk')).order_by('-created_at').values('created_at')[:1]
    if request.user.is_staff or request.user.is_superuser:
        recent_tickets = Ticket.objects.annotate(last_message_date=Subquery(last_message_subquery)).order_by('-last_message_date')[:4]
    else:
        recent_tickets = Ticket.objects.filter(user=request.user).annotate(last_message_date=Subquery(last_message_subquery)).order_by('-last_message_date')[:4]

    context = {
        'ticket_stats': ticket_stats,
        'profile': profile,
        'recent_tickets': recent_tickets,
        'is_admin': request.user.is_staff or request.user.is_superuser,
    }
    return render(request, 'tickets/home.html', context)


@login_required
def ticket_list(request):
    if request.user.is_staff or request.user.is_superuser:
        tickets = Ticket.objects.all().order_by('-created_at')
    else:
        tickets = Ticket.objects.filter(user=request.user).order_by('-created_at')

    page_number = request.GET.get('page')
    paginator = Paginator(tickets, 6)
    object_list = paginator.get_page(page_number)
    pages_to_show = get_pages_to_show(object_list.number, paginator.num_pages)

    context = {
        'tickets': object_list,
        'pages_to_show': pages_to_show,
        'is_admin': request.user.is_staff or request.user.is_superuser,
    }
    return render(request, 'tickets/ticket_list.html', context)


@login_required
def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket, id=pk)

    context = {
        'ticket': ticket,
        'is_admin': request.user.is_staff or request.user.is_superuser,
    }
    return render(request, 'tickets/ticket_detail.html', context)


@login_required
@require_POST
def reply_ticket(request, pk):
    ticket = get_object_or_404(Ticket, id=pk)
    message_text = request.POST.get('reply-message')
    attachment = request.FILES.get('reply-attachment')

    if message_text:
        ticket_message = TicketMessage.objects.create(
            ticket=ticket,
            user=request.user,
            message=message_text
        )

        if attachment:
            TicketAttachment.objects.create(
                message=ticket_message,
                file=attachment
            )

        is_admin = request.user.is_staff or request.user.is_superuser

        if is_admin:
            replied_status = TicketStatus.objects.get(name='پاسخ داده شده')
            ticket.status = replied_status
        else:
            last_message = ticket.messages.exclude(id=ticket_message.id).last()
            if last_message and (last_message.user.is_staff or last_message.user.is_superuser):
                in_progress_status = TicketStatus.objects.get(name='در حال بررسی')
                ticket.status = in_progress_status

        ticket.save()

    return redirect('tickets:ticket_detail', pk=ticket.id)


@login_required
@require_POST
def close_ticket(request, pk):
    ticket = get_object_or_404(Ticket, id=pk)

    if request.user.is_staff or request.user.is_superuser:
        closed_status = TicketStatus.objects.get(name='بسته شده')
        ticket.status = closed_status
        ticket.is_closed = True
        ticket.closed_at = timezone.now()
        ticket.save()

    return redirect('tickets:ticket_detail', pk=ticket.id)


@login_required
def new_ticket(request):
    departments = Department.objects.all()
    priorities = TicketPriority.objects.all()

    if request.method == 'POST':
        subject = request.POST.get('subject')
        department_id = request.POST.get('department')
        priority_id = request.POST.get('priority')
        message_text = request.POST.get('message')
        attachment = request.FILES.get('attachment')

        try:
            ticket = Ticket.objects.create(
                subject=subject,
                user=request.user,
                department_id=department_id,
                priority_id=priority_id,
                status=TicketStatus.objects.get(name='جدید')
            )

            ticket_message = TicketMessage.objects.create(
                ticket=ticket,
                user=request.user,
                message=message_text
            )

            if attachment:
                TicketAttachment.objects.create(
                    message=ticket_message,
                    file=attachment
                )

            return redirect('tickets:ticket_detail', pk=ticket.id)

        except Exception as e:
            messages.error(request, f'خطا در ایجاد تیکت: {str(e)}')

    context = {
        'departments': departments,
        'priorities': priorities,
    }
    return render(request, 'tickets/new_ticket.html', context)


@login_required
def ticket_search(request):
    tickets_search = request.GET.get('search')

    if request.user.is_staff or request.user.is_superuser:
        tickets = Ticket.objects.all().order_by('-created_at')
    else:
        tickets = Ticket.objects.filter(user=request.user, subject__icontains=tickets_search).order_by('-created_at')

    page_number = request.GET.get('page')
    paginator = Paginator(tickets, 6)
    object_list = paginator.get_page(page_number)
    pages_to_show = get_pages_to_show(object_list.number, paginator.num_pages)
    context = {
        'tickets': object_list,
        'pages_to_show': pages_to_show,
        'is_admin': request.user.is_staff or request.user.is_superuser,
    }
    return render(request, 'tickets/ticket_list.html', context)
