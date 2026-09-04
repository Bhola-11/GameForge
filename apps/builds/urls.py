from django.urls import path
from . import views

app_name = 'builds'

urlpatterns = [
    path('', views.BuildListView.as_view(), name='list'),
    path('create/', views.BuildCreateView.as_view(), name='create'),
    path('<int:pk>/', views.BuildDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.BuildUpdateView.as_view(), name='edit'),
]
