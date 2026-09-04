from django.urls import path
from . import views

app_name = 'bugs'

urlpatterns = [
    path('', views.BugListView.as_view(), name='list'),
    path('create/', views.BugCreateView.as_view(), name='create'),
    path('<int:pk>/', views.BugDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.BugUpdateView.as_view(), name='edit'),
    path('<int:pk>/comment/', views.add_bug_comment, name='add_comment'),
]
