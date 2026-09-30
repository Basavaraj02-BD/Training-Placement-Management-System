from django.urls import reverse_lazy
from django.db.models import Q
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from accounts.mixins import RoleRequiredMixin
from .models import Course, Student
from .forms import CourseForm, StudentForm


class StudentListView(RoleRequiredMixin, ListView):
    model = Student
    template_name = 'students/student_list.html'
    context_object_name = 'students'
    paginate_by = 12

    def get_queryset(self):
        qs = Student.objects.select_related('course', 'batch').all()
        q = self.request.GET.get('q', '').strip()
        status = self.request.GET.get('status', '')
        if q:
            qs = qs.filter(Q(first_name__icontains=q) | Q(last_name__icontains=q) |
                            Q(email__icontains=q) | Q(phone__icontains=q))
        if status:
            qs = qs.filter(status=status)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['q'] = self.request.GET.get('q', '')
        ctx['status'] = self.request.GET.get('status', '')
        ctx['status_choices'] = Student.Status.choices
        return ctx


class StudentDetailView(RoleRequiredMixin, DetailView):
    model = Student
    template_name = 'students/student_detail.html'
    context_object_name = 'student'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        student = self.object
        ctx['attendance_records'] = student.attendance_records.order_by('-date')[:15]
        ctx['test_results'] = student.test_results.select_related('test').order_by('-test__test_date')
        ctx['interviews'] = student.interviews.order_by('-interview_date')
        ctx['projects'] = student.projects.all()
        ctx['applications'] = student.applications.select_related('job', 'job__company').order_by('-applied_date')
        return ctx


class StudentCreateView(RoleRequiredMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('students:list')


class StudentUpdateView(RoleRequiredMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('students:list')


class StudentDeleteView(RoleRequiredMixin, DeleteView):
    model = Student
    template_name = 'partials/confirm_delete.html'
    success_url = reverse_lazy('students:list')


class CourseListView(RoleRequiredMixin, ListView):
    model = Course
    template_name = 'students/course_list.html'
    context_object_name = 'courses'


class CourseCreateView(RoleRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'students/course_form.html'
    success_url = reverse_lazy('students:course_list')


class CourseUpdateView(RoleRequiredMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'students/course_form.html'
    success_url = reverse_lazy('students:course_list')


class CourseDeleteView(RoleRequiredMixin, DeleteView):
    model = Course
    template_name = 'partials/confirm_delete.html'
    success_url = reverse_lazy('students:course_list')
