from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.TaskListView.as_view(), name='list'),
    path('board/', views.task_board_view, name='board'),
    path('create/', views.TaskCreateView.as_view(), name='create'),
    path('<int:pk>/', views.TaskDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.TaskUpdateView.as_view(), name='edit'),
    path('<int:pk>/update-status/', views.update_task_status_ajax, name='update_status'),
    path('<int:pk>/comment/', views.add_task_comment, name='add_comment'),
    path('<int:pk>/log-time/', views.log_task_time, name='log_time'),
]
