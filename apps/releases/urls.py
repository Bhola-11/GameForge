from django.urls import path
from . import views

app_name = 'releases'

urlpatterns = [
    path('', views.ReleaseListView.as_view(), name='list'),
    path('create/', views.ReleaseCreateView.as_view(), name='create'),
    path('<int:pk>/', views.ReleaseDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.ReleaseUpdateView.as_view(), name='edit'),
]
