from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from accounts.mixins import RoleRequiredMixin, AdminRequiredMixin
from .models import Company, JobPosting, Application
from .forms import CompanyForm, JobPostingForm, ApplicationForm


class CompanyListView(RoleRequiredMixin, ListView):
    model = Company
    template_name = 'placements/company_list.html'
    context_object_name = 'companies'


class CompanyCreateView(AdminRequiredMixin, CreateView):
    model = Company
    form_class = CompanyForm
    template_name = 'placements/company_form.html'
    success_url = reverse_lazy('placements:company_list')


class CompanyUpdateView(AdminRequiredMixin, UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = 'placements/company_form.html'
    success_url = reverse_lazy('placements:company_list')


class CompanyDeleteView(AdminRequiredMixin, DeleteView):
    model = Company
    template_name = 'partials/confirm_delete.html'
    success_url = reverse_lazy('placements:company_list')


class JobPostingListView(RoleRequiredMixin, ListView):
    model = JobPosting
    template_name = 'placements/job_list.html'
    context_object_name = 'jobs'

    def get_queryset(self):
        return JobPosting.objects.select_related('company').all()


class JobPostingDetailView(RoleRequiredMixin, DetailView):
    model = JobPosting
    template_name = 'placements/job_detail.html'
    context_object_name = 'job'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['applications'] = self.object.applications.select_related('student').all()
        return ctx


class JobPostingCreateView(AdminRequiredMixin, CreateView):
    model = JobPosting
    form_class = JobPostingForm
    template_name = 'placements/job_form.html'
    success_url = reverse_lazy('placements:job_list')


class JobPostingUpdateView(AdminRequiredMixin, UpdateView):
    model = JobPosting
    form_class = JobPostingForm
    template_name = 'placements/job_form.html'
    success_url = reverse_lazy('placements:job_list')


class JobPostingDeleteView(AdminRequiredMixin, DeleteView):
    model = JobPosting
    template_name = 'partials/confirm_delete.html'
    success_url = reverse_lazy('placements:job_list')


class ApplicationListView(RoleRequiredMixin, ListView):
    model = Application
    template_name = 'placements/application_list.html'
    context_object_name = 'applications'

    def get_queryset(self):
        qs = Application.objects.select_related('student', 'job', 'job__company').all()
        status = self.request.GET.get('status', '')
        if status:
            qs = qs.filter(selection_status=status)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['status'] = self.request.GET.get('status', '')
        ctx['status_choices'] = Application.SelectionStatus.choices
        return ctx


class ApplicationCreateView(AdminRequiredMixin, CreateView):
    model = Application
    form_class = ApplicationForm
    template_name = 'placements/application_form.html'
    success_url = reverse_lazy('placements:application_list')


class ApplicationUpdateView(AdminRequiredMixin, UpdateView):
    model = Application
    form_class = ApplicationForm
    template_name = 'placements/application_form.html'
    success_url = reverse_lazy('placements:application_list')


class ApplicationDeleteView(AdminRequiredMixin, DeleteView):
    model = Application
    template_name = 'partials/confirm_delete.html'
    success_url = reverse_lazy('placements:application_list')
