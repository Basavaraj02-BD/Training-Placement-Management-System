from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views import View

from accounts.mixins import RoleRequiredMixin
from batches.models import Batch
from .models import Attendance


class MarkAttendanceView(RoleRequiredMixin, View):
    template_name = 'attendance/mark_attendance.html'

    def get(self, request):
        batches = Batch.objects.all()
        batch_id = request.GET.get('batch', '')
        date_str = request.GET.get('date') or str(timezone.localdate())
        selected_batch = None
        students = []
        if batch_id:
            selected_batch = get_object_or_404(Batch, pk=batch_id)
            students = list(selected_batch.students.filter(status='ACTIVE'))
            existing = {a.student_id: a.status for a in
                        Attendance.objects.filter(batch=selected_batch, date=date_str)}
            for s in students:
                s.existing_status = existing.get(s.id, 'PRESENT')
        return render(request, self.template_name, {
            'batches': batches, 'selected_batch': selected_batch, 'batch_id': batch_id,
            'students': students, 'date': date_str,
        })

    def post(self, request):
        batch_id = request.POST.get('batch')
        date_str = request.POST.get('date')
        batch = get_object_or_404(Batch, pk=batch_id)
        students = batch.students.filter(status='ACTIVE')
        saved = 0
        for student in students:
            status = request.POST.get(f'status_{student.id}')
            if status in (Attendance.Status.PRESENT, Attendance.Status.ABSENT):
                Attendance.objects.update_or_create(
                    student=student, date=date_str,
                    defaults={'batch': batch, 'status': status, 'marked_by': request.user},
                )
                saved += 1
        messages.success(request, f"Attendance saved for {saved} student(s) in {batch.name} on {date_str}.")
        return redirect(f"{reverse('attendance:mark')}?batch={batch_id}&date={date_str}")


class AttendanceHistoryView(RoleRequiredMixin, View):
    template_name = 'attendance/history.html'

    def get(self, request):
        batches = Batch.objects.all()
        batch_id = request.GET.get('batch', '')
        records = Attendance.objects.select_related('student', 'batch').all()
        if batch_id:
            records = records.filter(batch_id=batch_id)
        records = records[:200]
        return render(request, self.template_name, {
            'batches': batches, 'batch_id': batch_id, 'records': records,
        })


class AttendanceReportView(RoleRequiredMixin, View):
    template_name = 'attendance/report.html'

    def get(self, request):
        batches = Batch.objects.all()
        batch_id = request.GET.get('batch', '')
        report_rows = []
        selected_batch = None
        if batch_id:
            selected_batch = get_object_or_404(Batch, pk=batch_id)
            for student in selected_batch.students.all():
                report_rows.append({
                    'student': student,
                    'percentage': student.attendance_percentage,
                    'total': student.attendance_records.filter(batch=selected_batch).count(),
                    'present': student.attendance_records.filter(batch=selected_batch, status='PRESENT').count(),
                })
        return render(request, self.template_name, {
            'batches': batches, 'batch_id': batch_id, 'selected_batch': selected_batch,
            'report_rows': report_rows,
        })


class LowAttendanceView(RoleRequiredMixin, View):
    template_name = 'attendance/low_attendance.html'
    THRESHOLD = 75

    def get(self, request):
        from students.models import Student
        rows = []
        for student in Student.objects.filter(status='ACTIVE'):
            pct = student.attendance_percentage
            if pct is not None and pct < self.THRESHOLD:
                rows.append({'student': student, 'percentage': pct})
        rows.sort(key=lambda r: r['percentage'])
        return render(request, self.template_name, {'rows': rows, 'threshold': self.THRESHOLD})
