from django.conf import settings
from django.db import models


class Project(models.Model):
    class Status(models.TextChoices):
        NOT_STARTED = 'NOT_STARTED', 'Not started'
        IN_PROGRESS = 'IN_PROGRESS', 'In progress'
        SUBMITTED = 'SUBMITTED', 'Submitted'
        EVALUATED = 'EVALUATED', 'Evaluated'
        COMPLETED = 'COMPLETED', 'Completed'

    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    batch = models.ForeignKey('batches.Batch', on_delete=models.SET_NULL, null=True, blank=True, related_name='projects')
    students = models.ManyToManyField('students.Student', related_name='projects', blank=True)
    start_date = models.DateField(null=True, blank=True)
    submission_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.NOT_STARTED)
    trainer_evaluation = models.TextField(blank=True)
    evaluation_score = models.PositiveIntegerField(null=True, blank=True, help_text="Score out of 100")
    evaluated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return self.title
