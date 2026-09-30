from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from accounts.mixins import RoleRequiredMixin
from .models import MockTest, MockTestResult
from .forms import MockTestForm


class MockTestListView(RoleRequiredMixin, ListView):
    model = MockTest
    template_name = 'mocktests/test_list.html'
    context_object_name = 'tests'

    def get_queryset(self):
        return MockTest.objects.select_related('batch').all()


class MockTestDetailView(RoleRequiredMixin, DetailView):
    model = MockTest
    template_name = 'mocktests/test_detail.html'
    context_object_name = 'test'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['results'] = self.object.results.select_related('student').all()
        return ctx


class MockTestCreateView(RoleRequiredMixin, CreateView):
    model = MockTest
    form_class = MockTestForm
    template_name = 'mocktests/test_form.html'
    success_url = reverse_lazy('mocktests:list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class MockTestUpdateView(RoleRequiredMixin, UpdateView):
    model = MockTest
    form_class = MockTestForm
    template_name = 'mocktests/test_form.html'
    success_url = reverse_lazy('mocktests:list')


class MockTestDeleteView(RoleRequiredMixin, DeleteView):
    model = MockTest
    template_name = 'partials/confirm_delete.html'
    success_url = reverse_lazy('mocktests:list')


class RecordResultsView(RoleRequiredMixin, View):
    template_name = 'mocktests/record_results.html'

    def get(self, request, pk):
        test = get_object_or_404(MockTest, pk=pk)
        students = list(test.batch.students.filter(status='ACTIVE'))
        existing = {r.student_id: r.marks_obtained for r in test.results.all()}
        for s in students:
            s.existing_marks = existing.get(s.id, '')
        return render(request, self.template_name, {'test': test, 'students': students})

    def post(self, request, pk):
        test = get_object_or_404(MockTest, pk=pk)
        students = test.batch.students.filter(status='ACTIVE')
        saved = 0
        for student in students:
            marks = request.POST.get(f'marks_{student.id}', '').strip()
            if marks != '':
                MockTestResult.objects.update_or_create(
                    test=test, student=student, defaults={'marks_obtained': marks},
                )
                saved += 1
        messages.success(request, f"Results saved for {saved} student(s).")
        return redirect(reverse('mocktests:detail', args=[test.pk]))
