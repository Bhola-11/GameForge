from django.urls import path
from . import views

app_name = 'assets'

urlpatterns = [
    path('', views.AssetListView.as_view(), name='list'),
    path('create/', views.AssetCreateView.as_view(), name='create'),
    path('<int:pk>/', views.AssetDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.AssetUpdateView.as_view(), name='edit'),
]
