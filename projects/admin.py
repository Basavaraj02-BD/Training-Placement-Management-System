from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'batch', 'status', 'submission_date', 'evaluation_score')
    list_filter = ('status', 'batch')
    filter_horizontal = ('students',)
    search_fields = ('title',)
