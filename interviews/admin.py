from django.contrib import admin
from .models import MockInterview


@admin.register(MockInterview)
class MockInterviewAdmin(admin.ModelAdmin):
    list_display = ('student', 'round_type', 'interview_date', 'interview_time', 'interviewer_name', 'attended', 'score')
    list_filter = ('round_type', 'attended', 'interview_date')
    search_fields = ('student__first_name', 'student__last_name', 'interviewer_name')
