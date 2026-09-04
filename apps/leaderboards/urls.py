from django.urls import path
from . import views

app_name = 'leaderboards'

urlpatterns = [
    path('', views.LeaderboardListView.as_view(), name='list'),
    path('create/', views.LeaderboardCreateView.as_view(), name='create'),
    path('<int:pk>/', views.LeaderboardDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.LeaderboardUpdateView.as_view(), name='edit'),
]
