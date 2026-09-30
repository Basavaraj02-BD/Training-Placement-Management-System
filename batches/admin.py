from django.contrib import admin
from .models import Batch


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'trainer', 'status', 'start_date', 'end_date')
    list_filter = ('status', 'course')
    search_fields = ('name',)
