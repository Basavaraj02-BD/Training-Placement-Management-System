from django import forms
from common.forms import BootstrapFormMixin
from .models import MockTest


class MockTestForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = MockTest
        fields = ['batch', 'topic', 'test_date', 'test_time', 'total_marks']
        widgets = {
            'test_date': forms.DateInput(attrs={'type': 'date'}),
            'test_time': forms.TimeInput(attrs={'type': 'time'}),
        }
