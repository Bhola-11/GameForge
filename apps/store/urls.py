from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.StoreListView.as_view(), name='list'),
    path('create/', views.StoreCreateView.as_view(), name='create'),
    path('<int:pk>/', views.StoreDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.StoreUpdateView.as_view(), name='edit'),
]
