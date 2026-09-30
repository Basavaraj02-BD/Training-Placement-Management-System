from django import forms
from common.forms import BootstrapFormMixin
from .models import Batch


class BatchForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Batch
        fields = ['name', 'course', 'trainer', 'timing', 'start_date', 'end_date', 'max_students', 'status']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
