from django import forms
from common.forms import BootstrapFormMixin
from .models import Course, Student


class CourseForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'duration_weeks', 'description']


class StudentForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'phone', 'gender', 'date_of_birth',
                   'address', 'photo', 'course', 'batch', 'status']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 2}),
        }
