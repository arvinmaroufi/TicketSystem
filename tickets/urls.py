from django.urls import path
from . import views


app_name = 'tickets'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('tickets/', views.ticket_list, name='ticket_list'),
    path('tickets/<int:pk>/', views.ticket_detail, name='ticket_detail'),
    path('tickets/<int:pk>/reply/', views.reply_ticket, name='reply_ticket'),
    path('tickets/<int:pk>/close/', views.close_ticket, name='close_ticket'),
    path('tickets/new_ticket/', views.new_ticket, name='new_ticket'),
    path('ticketss/', views.ticket_search, name='ticket_search'),
]
