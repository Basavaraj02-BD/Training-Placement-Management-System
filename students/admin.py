from django.contrib import admin
from .models import Course, Student


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration_weeks')
    search_fields = ('name',)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'course', 'batch', 'status')
    list_filter = ('status', 'course', 'batch', 'gender')
    search_fields = ('first_name', 'last_name', 'email', 'phone')
