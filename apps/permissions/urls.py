from django.urls import path
from . import views

app_name = 'permissions'

urlpatterns = [
    path('matrix/', views.permissions_matrix_view, name='matrix'),
]
