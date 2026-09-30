from django.contrib import admin
from .models import MockTest, MockTestResult


class ResultInline(admin.TabularInline):
    model = MockTestResult
    extra = 0


@admin.register(MockTest)
class MockTestAdmin(admin.ModelAdmin):
    list_display = ('topic', 'batch', 'test_date', 'test_time', 'total_marks')
    list_filter = ('batch',)
    inlines = [ResultInline]


@admin.register(MockTestResult)
class MockTestResultAdmin(admin.ModelAdmin):
    list_display = ('test', 'student', 'marks_obtained')
