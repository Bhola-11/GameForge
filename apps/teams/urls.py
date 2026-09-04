from django.urls import path
from . import views

app_name = 'teams'

urlpatterns = [
    path('', views.TeamListView.as_view(), name='list'),
    path('create/', views.TeamCreateView.as_view(), name='create'),
    path('<int:pk>/', views.TeamDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.TeamUpdateView.as_view(), name='edit'),
    path('<int:pk>/add-member/', views.add_team_member_view, name='add_member'),
]
