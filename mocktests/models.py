from django.conf import settings
from django.db import models


class MockTest(models.Model):
    batch = models.ForeignKey('batches.Batch', on_delete=models.CASCADE, related_name='mock_tests')
    topic = models.CharField(max_length=150)
    test_date = models.DateField()
    test_time = models.TimeField()
    total_marks = models.PositiveIntegerField(default=100)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-test_date', '-test_time']

    def __str__(self):
        return f"{self.topic} ({self.batch})"

    @property
    def average_score(self):
        agg = self.results.aggregate(models.Avg('marks_obtained'))
        val = agg['marks_obtained__avg']
        return round(val, 1) if val is not None else None


class MockTestResult(models.Model):
    test = models.ForeignKey(MockTest, on_delete=models.CASCADE, related_name='results')
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='test_results')
    marks_obtained = models.DecimalField(max_digits=6, decimal_places=2)
    remarks = models.CharField(max_length=200, blank=True)

    class Meta:
        unique_together = ('test', 'student')
        ordering = ['-marks_obtained']

    def __str__(self):
        return f"{self.student} - {self.test} - {self.marks_obtained}"

    @property
    def percentage(self):
        if not self.test.total_marks:
            return None
        return round((float(self.marks_obtained) / self.test.total_marks) * 100, 1)
