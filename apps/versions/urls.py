from django.urls import path
from . import views

app_name = 'versions'

urlpatterns = [
    path('', views.VersionListView.as_view(), name='list'),
    path('create/', views.VersionCreateView.as_view(), name='create'),
    path('<int:pk>/', views.VersionDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.VersionUpdateView.as_view(), name='edit'),
]
