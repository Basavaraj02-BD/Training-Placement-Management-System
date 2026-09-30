from django import forms
from common.forms import BootstrapFormMixin
from .models import MockInterview


class MockInterviewForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = MockInterview
        fields = ['student', 'batch', 'interview_date', 'interview_time', 'interviewer_name', 'round_type']
        widgets = {
            'interview_date': forms.DateInput(attrs={'type': 'date'}),
            'interview_time': forms.TimeInput(attrs={'type': 'time'}),
        }


class InterviewFeedbackForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = MockInterview
        fields = ['attended', 'feedback', 'score']
        widgets = {'feedback': forms.Textarea(attrs={'rows': 4})}
