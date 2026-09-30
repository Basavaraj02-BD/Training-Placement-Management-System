from django import forms
from common.forms import BootstrapFormMixin
from .models import Project


class ProjectForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'batch', 'students', 'start_date', 'submission_date', 'status']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'submission_date': forms.DateInput(attrs={'type': 'date'}),
            'students': forms.SelectMultiple(attrs={'size': 8}),
        }


class ProjectEvaluationForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Project
        fields = ['status', 'trainer_evaluation', 'evaluation_score']
        widgets = {'trainer_evaluation': forms.Textarea(attrs={'rows': 4})}
