from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=120, unique=True)
    duration_weeks = models.PositiveIntegerField(default=8)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Student(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        INACTIVE = 'INACTIVE', 'Inactive'
        COMPLETED = 'COMPLETED', 'Completed'
        PLACED = 'PLACED', 'Placed'
        DROPPED = 'DROPPED', 'Dropped'

    class Gender(models.TextChoices):
        MALE = 'M', 'Male'
        FEMALE = 'F', 'Female'
        OTHER = 'O', 'Other'

    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=1, choices=Gender.choices, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255, blank=True)
    photo = models.ImageField(upload_to='student_photos/', null=True, blank=True)

    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, related_name='students')
    batch = models.ForeignKey('batches.Batch', on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)

    enrollment_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['first_name', 'last_name']

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def attendance_percentage(self):
        total = self.attendance_records.count()
        if not total:
            return None
        present = self.attendance_records.filter(status='PRESENT').count()
        return round((present / total) * 100, 1)
