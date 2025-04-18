from django.db import models
from django.contrib.auth.models import User


class Department(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام دپارتمان")
    description = models.TextField(blank=True, verbose_name="توضیحات")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "دپارتمان"
        verbose_name_plural = "دپارتمان ‌ها"


class TicketPriority(models.Model):
    name = models.CharField(max_length=50, verbose_name="نام اولویت")
    color = models.CharField(max_length=20, verbose_name="کد رنگ")
    order = models.IntegerField(verbose_name="ترتیب")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "اولویت تیکت"
        verbose_name_plural = "اولویت ‌های تیکت"


class TicketStatus(models.Model):
    name = models.CharField(max_length=50, verbose_name="نام وضعیت")
    color = models.CharField(max_length=20, verbose_name="کد رنگ")
    is_closed = models.BooleanField(default=False, verbose_name="وضعیت بسته شده")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "وضعیت تیکت"
        verbose_name_plural = "وضعیت ‌های تیکت"


class Ticket(models.Model):
    subject = models.CharField(max_length=200, verbose_name="موضوع")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets', verbose_name="کاربر")
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, verbose_name="دپارتمان")
    priority = models.ForeignKey(TicketPriority, on_delete=models.SET_NULL, null=True, verbose_name="اولویت")
    status = models.ForeignKey(TicketStatus, on_delete=models.SET_NULL, null=True, verbose_name="وضعیت")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")
    is_closed = models.BooleanField(default=False, verbose_name="بسته شده")
    closed_at = models.DateTimeField(null=True, blank=True, verbose_name="تاریخ بسته شدن")

    def __str__(self):
        return f"{self.subject} - {self.user.username}"

    class Meta:
        verbose_name = "تیکت"
        verbose_name_plural = "تیکت‌ها"
        ordering = ['-created_at']


class TicketMessage(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='messages', verbose_name="تیکت")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    message = models.TextField(verbose_name="پیام")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    is_internal = models.BooleanField(default=False, verbose_name="پیام داخلی")

    def save(self, *args, **kwargs):
        if not self.user_id:
            self.user = self.ticket.user
        super().save(*args, **kwargs)

    def __str__(self):
        return f"پیام برای تیکت #{self.ticket.id}"

    class Meta:
        verbose_name = "پیام تیکت"
        verbose_name_plural = "پیام‌ های تیکت"
        ordering = ['created_at']


class TicketAttachment(models.Model):
    message = models.ForeignKey(TicketMessage, on_delete=models.CASCADE, related_name='attachments', verbose_name="پیام")
    file = models.FileField(upload_to='ticket_attachments/', verbose_name="فایل")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ آپلود")

    def __str__(self):
        return f"پیوست برای پیام #{self.message.id}"

    class Meta:
        verbose_name = "پیوست تیکت"
        verbose_name_plural = "پیوست‌ های تیکت"

