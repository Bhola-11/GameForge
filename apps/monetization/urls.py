from django.urls import path
from . import views

app_name = 'monetization'

urlpatterns = [
    path('', views.monetization_dashboard_view, name='dashboard'),
    path('items/create/', views.InGameItemCreateView.as_view(), name='item_create'),
]
