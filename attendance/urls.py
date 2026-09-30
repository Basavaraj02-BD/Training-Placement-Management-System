from django.urls import path
from . import views

app_name = 'attendance'
urlpatterns = [
    path('', views.MarkAttendanceView.as_view(), name='mark'),
    path('history/', views.AttendanceHistoryView.as_view(), name='history'),
    path('report/', views.AttendanceReportView.as_view(), name='report'),
    path('low/', views.LowAttendanceView.as_view(), name='low'),
]
