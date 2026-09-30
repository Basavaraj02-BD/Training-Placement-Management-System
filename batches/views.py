from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from accounts.mixins import RoleRequiredMixin, AdminRequiredMixin
from .models import Batch
from .forms import BatchForm


class BatchListView(RoleRequiredMixin, ListView):
    model = Batch
    template_name = 'batches/batch_list.html'
    context_object_name = 'batches'

    def get_queryset(self):
        qs = Batch.objects.select_related('course', 'trainer').all()
        status = self.request.GET.get('status', '')
        if status:
            qs = qs.filter(status=status)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['status'] = self.request.GET.get('status', '')
        ctx['status_choices'] = Batch.Status.choices
        return ctx


class BatchDetailView(RoleRequiredMixin, DetailView):
    model = Batch
    template_name = 'batches/batch_detail.html'
    context_object_name = 'batch'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['roster'] = self.object.students.all()
        return ctx


class BatchCreateView(AdminRequiredMixin, CreateView):
    model = Batch
    form_class = BatchForm
    template_name = 'batches/batch_form.html'
    success_url = reverse_lazy('batches:list')


class BatchUpdateView(AdminRequiredMixin, UpdateView):
    model = Batch
    form_class = BatchForm
    template_name = 'batches/batch_form.html'
    success_url = reverse_lazy('batches:list')


class BatchDeleteView(AdminRequiredMixin, DeleteView):
    model = Batch
    template_name = 'partials/confirm_delete.html'
    success_url = reverse_lazy('batches:list')
