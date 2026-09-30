from django.urls import path
from . import views

app_name = 'batches'
urlpatterns = [
    path('', views.BatchListView.as_view(), name='list'),
    path('add/', views.BatchCreateView.as_view(), name='add'),
    path('<int:pk>/', views.BatchDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.BatchUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.BatchDeleteView.as_view(), name='delete'),
]
