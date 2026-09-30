from django import forms
from common.forms import BootstrapFormMixin


class AttendanceFilterForm(BootstrapFormMixin, forms.Form):
    batch = forms.ChoiceField(required=False)
    date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
