from django.urls import path
from . import views

app_name = 'achievements'

urlpatterns = [
    path('', views.AchievementListView.as_view(), name='list'),
    path('create/', views.AchievementCreateView.as_view(), name='create'),
    path('<int:pk>/', views.AchievementDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.AchievementUpdateView.as_view(), name='edit'),
]
