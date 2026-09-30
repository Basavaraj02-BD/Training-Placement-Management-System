from django.contrib import admin
from .models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'batch', 'date', 'status', 'marked_by')
    list_filter = ('status', 'batch', 'date')
    search_fields = ('student__first_name', 'student__last_name')
