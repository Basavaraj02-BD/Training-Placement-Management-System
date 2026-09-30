from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from accounts.mixins import RoleRequiredMixin
from .models import MockInterview
from .forms import MockInterviewForm, InterviewFeedbackForm


class InterviewListView(RoleRequiredMixin, ListView):
    model = MockInterview
    template_name = 'interviews/interview_list.html'
    context_object_name = 'interviews'

    def get_queryset(self):
        qs = MockInterview.objects.select_related('student', 'batch').all()
        round_type = self.request.GET.get('round', '')
        if round_type:
            qs = qs.filter(round_type=round_type)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['round'] = self.request.GET.get('round', '')
        ctx['round_choices'] = MockInterview.RoundType.choices
        return ctx


class InterviewCreateView(RoleRequiredMixin, CreateView):
    model = MockInterview
    form_class = MockInterviewForm
    template_name = 'interviews/interview_form.html'
    success_url = reverse_lazy('interviews:list')

    def form_valid(self, form):
        form.instance.scheduled_by = self.request.user
        return super().form_valid(form)


class InterviewUpdateView(RoleRequiredMixin, UpdateView):
    model = MockInterview
    form_class = MockInterviewForm
    template_name = 'interviews/interview_form.html'
    success_url = reverse_lazy('interviews:list')


class InterviewFeedbackView(RoleRequiredMixin, UpdateView):
    model = MockInterview
    form_class = InterviewFeedbackForm
    template_name = 'interviews/interview_feedback_form.html'
    success_url = reverse_lazy('interviews:list')


class InterviewDeleteView(RoleRequiredMixin, DeleteView):
    model = MockInterview
    template_name = 'partials/confirm_delete.html'
    success_url = reverse_lazy('interviews:list')
