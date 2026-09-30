from django.urls import path
from . import views

app_name = 'interviews'
urlpatterns = [
    path('', views.InterviewListView.as_view(), name='list'),
    path('add/', views.InterviewCreateView.as_view(), name='add'),
    path('<int:pk>/edit/', views.InterviewUpdateView.as_view(), name='edit'),
    path('<int:pk>/feedback/', views.InterviewFeedbackView.as_view(), name='feedback'),
    path('<int:pk>/delete/', views.InterviewDeleteView.as_view(), name='delete'),
]
