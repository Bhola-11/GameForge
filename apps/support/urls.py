from django.urls import path
from . import views

app_name = 'support'

urlpatterns = [
    path('', views.SupportTicketListView.as_view(), name='list'),
    path('create/', views.SupportTicketCreateView.as_view(), name='create'),
    path('<int:pk>/', views.SupportTicketDetailView.as_view(), name='detail'),
    path('<int:pk>/reply/', views.add_ticket_reply, name='add_reply'),
]
