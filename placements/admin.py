from django.contrib import admin
from .models import Company, JobPosting, Application


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_email', 'contact_phone')
    search_fields = ('name',)


@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ('job_role', 'company', 'job_code', 'ctc_offered', 'status', 'posted_date')
    list_filter = ('status', 'company')
    search_fields = ('job_role', 'job_code')


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('student', 'job', 'interview_status', 'selection_status', 'offer_ctc')
    list_filter = ('interview_status', 'selection_status')
