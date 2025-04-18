from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Ticket


@login_required
def dashboard(request):
    ticket_stats = {
        'new': Ticket.objects.filter(user=request.user, status__name='جدید').count(),
        'in_progress': Ticket.objects.filter(user=request.user, status__name='در حال بررسی').count(),
        'resolved': Ticket.objects.filter(user=request.user, status__name='حل شده').count(),
        'closed': Ticket.objects.filter(user=request.user, status__name='بسته شده').count(),
    }

    recent_tickets = Ticket.objects.filter(user=request.user).order_by('-created_at')[:5]

    context = {
        'ticket_stats': ticket_stats,
        'recent_tickets': recent_tickets,
    }
    return render(request, 'tickets/home.html', context)


