from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=150, unique=True)
    website = models.URLField(blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=15, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.name


class JobPosting(models.Model):
    class Status(models.TextChoices):
        OPEN = 'OPEN', 'Open'
        CLOSED = 'CLOSED', 'Closed'

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='job_postings')
    job_role = models.CharField(max_length=150)
    job_code = models.CharField(max_length=40, unique=True)
    description = models.TextField(blank=True)
    ctc_offered = models.DecimalField(max_digits=6, decimal_places=2, help_text="Annual CTC in LPA (Lakhs Per Annum)")
    eligibility_criteria = models.CharField(max_length=255, blank=True)
    posted_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.OPEN)

    class Meta:
        ordering = ['-posted_date']

    def __str__(self):
        return f"{self.job_role} @ {self.company} ({self.job_code})"


class Application(models.Model):
    class InterviewStatus(models.TextChoices):
        NOT_SCHEDULED = 'NOT_SCHEDULED', 'Not scheduled'
        SCHEDULED = 'SCHEDULED', 'Scheduled'
        COMPLETED = 'COMPLETED', 'Completed'

    class SelectionStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        SHORTLISTED = 'SHORTLISTED', 'Shortlisted'
        SELECTED = 'SELECTED', 'Selected'
        REJECTED = 'REJECTED', 'Rejected'
        ON_HOLD = 'ON_HOLD', 'On hold'

    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='applications')
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='applications')
    applied_date = models.DateField(auto_now_add=True)
    interview_status = models.CharField(max_length=15, choices=InterviewStatus.choices,
                                         default=InterviewStatus.NOT_SCHEDULED)
    selection_status = models.CharField(max_length=15, choices=SelectionStatus.choices,
                                         default=SelectionStatus.PENDING)
    offer_ctc = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True,
                                     help_text="Final offer CTC in LPA, if selected")
    remarks = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-applied_date']
        unique_together = ('student', 'job')

    def __str__(self):
        return f"{self.student} -> {self.job}"
