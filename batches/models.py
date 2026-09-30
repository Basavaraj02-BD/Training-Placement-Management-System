from django.conf import settings
from django.db import models


class Batch(models.Model):
    class Status(models.TextChoices):
        UPCOMING = 'UPCOMING', 'Upcoming'
        ONGOING = 'ONGOING', 'Ongoing'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'

    name = models.CharField(max_length=120, unique=True)
    course = models.ForeignKey('students.Course', on_delete=models.SET_NULL, null=True, related_name='batches')
    trainer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                 limit_choices_to={'role': 'TRAINER'}, related_name='batches_trained')
    timing = models.CharField(max_length=120, help_text="e.g. Mon-Fri, 9:00 AM - 12:00 PM")
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    max_students = models.PositiveIntegerField(default=30)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.UPCOMING)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return self.name

    @property
    def student_count(self):
        return self.students.count()
