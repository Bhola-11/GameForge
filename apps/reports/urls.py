from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.report_list_view, name='list'),
    path('<int:pk>/', views.report_detail_view, name='detail'),
]
