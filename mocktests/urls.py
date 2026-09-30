from django.urls import path
from . import views

app_name = 'mocktests'
urlpatterns = [
    path('', views.MockTestListView.as_view(), name='list'),
    path('add/', views.MockTestCreateView.as_view(), name='add'),
    path('<int:pk>/', views.MockTestDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.MockTestUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.MockTestDeleteView.as_view(), name='delete'),
    path('<int:pk>/results/', views.RecordResultsView.as_view(), name='results'),
]
