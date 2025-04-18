from django.contrib import admin
from . import models


@admin.register(models.Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(models.TicketPriority)
class TicketPriorityAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'order']
    list_editable = ['order']


@admin.register(models.TicketStatus)
class TicketStatusAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'is_closed']
    list_filter = ['is_closed']


class TicketMessageInline(admin.TabularInline):
    model = models.TicketMessage
    extra = 0
    readonly_fields = ['user', 'created_at']


@admin.register(models.Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['subject', 'user', 'department', 'status', 'priority', 'created_at']
    list_filter = ['status', 'priority', 'department', 'created_at']
    search_fields = ['subject', 'user__username']
    inlines = [TicketMessageInline]


