from django.urls import path
from . import views

app_name = 'organizations'

urlpatterns = [
    path('', views.OrgListView.as_view(), name='list'),
    path('create/', views.OrgCreateView.as_view(), name='create'),
    path('<int:pk>/', views.OrgDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.OrgUpdateView.as_view(), name='edit'),
    path('<int:pk>/invite/', views.invite_member_view, name='invite'),
]
