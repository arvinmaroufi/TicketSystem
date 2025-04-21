from django.urls import path
from . import views


app_name = 'tickets'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('tickets/', views.ticket_list, name='ticket_list'),
    path('tickets/<tid>/', views.ticket_detail, name='ticket_detail'),
    path('tickets/<tid>/reply/', views.reply_ticket, name='reply_ticket'),
    path('tickets/<tid>/close/', views.close_ticket, name='close_ticket'),
    path('new_ticket/', views.new_ticket, name='new_ticket'),
    path('ticket_search/', views.ticket_search, name='ticket_search'),
    path('users/', views.user_list, name='user_list'),
    path('delete_user/<str:username>/', views.delete_user, name='delete_user'),
    path('edit_profile/<str:username>/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),
]
