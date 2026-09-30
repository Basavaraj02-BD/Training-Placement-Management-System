from django.urls import path
from . import views

app_name = 'placements'
urlpatterns = [
    path('companies/', views.CompanyListView.as_view(), name='company_list'),
    path('companies/add/', views.CompanyCreateView.as_view(), name='company_add'),
    path('companies/<int:pk>/edit/', views.CompanyUpdateView.as_view(), name='company_edit'),
    path('companies/<int:pk>/delete/', views.CompanyDeleteView.as_view(), name='company_delete'),

    path('jobs/', views.JobPostingListView.as_view(), name='job_list'),
    path('jobs/add/', views.JobPostingCreateView.as_view(), name='job_add'),
    path('jobs/<int:pk>/', views.JobPostingDetailView.as_view(), name='job_detail'),
    path('jobs/<int:pk>/edit/', views.JobPostingUpdateView.as_view(), name='job_edit'),
    path('jobs/<int:pk>/delete/', views.JobPostingDeleteView.as_view(), name='job_delete'),

    path('applications/', views.ApplicationListView.as_view(), name='application_list'),
    path('applications/add/', views.ApplicationCreateView.as_view(), name='application_add'),
    path('applications/<int:pk>/edit/', views.ApplicationUpdateView.as_view(), name='application_edit'),
    path('applications/<int:pk>/delete/', views.ApplicationDeleteView.as_view(), name='application_delete'),
]
