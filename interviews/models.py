from django.conf import settings
from django.db import models


class MockInterview(models.Model):
    class RoundType(models.TextChoices):
        TECHNICAL = 'TECHNICAL', 'Technical'
        HR = 'HR', 'HR'

    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='interviews')
    batch = models.ForeignKey('batches.Batch', on_delete=models.SET_NULL, null=True, blank=True, related_name='interviews')
    interview_date = models.DateField()
    interview_time = models.TimeField()
    interviewer_name = models.CharField(max_length=120)
    round_type = models.CharField(max_length=10, choices=RoundType.choices, default=RoundType.TECHNICAL)
    attended = models.BooleanField(default=False)
    feedback = models.TextField(blank=True)
    score = models.PositiveIntegerField(null=True, blank=True, help_text="Score out of 10")
    scheduled_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-interview_date', '-interview_time']

    def __str__(self):
        return f"{self.student} - {self.get_round_type_display()} - {self.interview_date}"
