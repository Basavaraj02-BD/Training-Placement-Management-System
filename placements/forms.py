from django import forms
from common.forms import BootstrapFormMixin
from .models import Company, JobPosting, Application


class CompanyForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'website', 'contact_email', 'contact_phone', 'notes']
        widgets = {'notes': forms.Textarea(attrs={'rows': 3})}


class JobPostingForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = JobPosting
        fields = ['company', 'job_role', 'job_code', 'description', 'ctc_offered',
                   'eligibility_criteria', 'status']
        widgets = {'description': forms.Textarea(attrs={'rows': 3})}


class ApplicationForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Application
        fields = ['student', 'job', 'interview_status', 'selection_status', 'offer_ctc', 'remarks']
