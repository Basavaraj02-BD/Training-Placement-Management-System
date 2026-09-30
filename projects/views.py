from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from accounts.mixins import RoleRequiredMixin
from .models import Project
from .forms import ProjectForm, ProjectEvaluationForm


class ProjectListView(RoleRequiredMixin, ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        qs = Project.objects.select_related('batch').all()
        status = self.request.GET.get('status', '')
        if status:
            qs = qs.filter(status=status)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['status'] = self.request.GET.get('status', '')
        ctx['status_choices'] = Project.Status.choices
        return ctx


class ProjectDetailView(RoleRequiredMixin, DetailView):
    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'


class ProjectCreateView(RoleRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('projects:list')


class ProjectUpdateView(RoleRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('projects:list')


class ProjectEvaluationView(RoleRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectEvaluationForm
    template_name = 'projects/project_evaluation_form.html'
    success_url = reverse_lazy('projects:list')

    def form_valid(self, form):
        form.instance.evaluated_by = self.request.user
        return super().form_valid(form)


class ProjectDeleteView(RoleRequiredMixin, DeleteView):
    model = Project
    template_name = 'partials/confirm_delete.html'
    success_url = reverse_lazy('projects:list')
