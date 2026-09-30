import datetime
import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.utils import timezone
from django.views.generic import TemplateView

from students.models import Student
from batches.models import Batch
from attendance.models import Attendance
from mocktests.models import MockTest
from interviews.models import MockInterview
from projects.models import Project
from placements.models import Application


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/home.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        today = timezone.localdate()

        today_qs = Attendance.objects.filter(date=today)
        today_total = today_qs.count()
        today_present = today_qs.filter(status='PRESENT').count()
        today_pct = round((today_present / today_total) * 100, 1) if today_total else None

        overall_total = Attendance.objects.count()
        overall_present = Attendance.objects.filter(status='PRESENT').count()
        overall_pct = round((overall_present / overall_total) * 100, 1) if overall_total else None

        ctx.update({
            'total_students': Student.objects.count(),
            'active_students': Student.objects.filter(status='ACTIVE').count(),
            'active_batches': Batch.objects.filter(status='ONGOING').count(),
            'total_batches': Batch.objects.count(),
            'today_present': today_present,
            'today_total': today_total,
            'today_pct': today_pct,
            'overall_pct': overall_pct,
            'upcoming_tests': MockTest.objects.filter(test_date__gte=today).select_related('batch')[:5],
            'upcoming_interviews': MockInterview.objects.filter(interview_date__gte=today).select_related('student')[:5],
            'pending_projects': Project.objects.exclude(status='COMPLETED').count(),
            'total_projects': Project.objects.count(),
            'total_placed': Application.objects.filter(selection_status='SELECTED').count(),
            'total_applications': Application.objects.count(),
            'placement_stats': Application.objects.values('selection_status').annotate(count=Count('id')),
        })

        trend_labels, trend_values = [], []
        for i in range(13, -1, -1):
            d = today - datetime.timedelta(days=i)
            day_qs = Attendance.objects.filter(date=d)
            day_total = day_qs.count()
            day_present = day_qs.filter(status='PRESENT').count()
            pct = round((day_present / day_total) * 100, 1) if day_total else None
            trend_labels.append(d.strftime('%b %d'))
            trend_values.append(pct)

        pipeline = list(ctx['placement_stats'])
        pipeline_labels = [p['selection_status'].replace('_', ' ').title() for p in pipeline]
        pipeline_values = [p['count'] for p in pipeline]

        ctx['trend_labels_json'] = json.dumps(trend_labels)
        ctx['trend_values_json'] = json.dumps(trend_values)
        ctx['pipeline_labels_json'] = json.dumps(pipeline_labels)
        ctx['pipeline_values_json'] = json.dumps(pipeline_values)
        return ctx
