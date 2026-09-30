import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import User
from students.models import Course, Student
from batches.models import Batch
from attendance.models import Attendance
from mocktests.models import MockTest, MockTestResult
from interviews.models import MockInterview
from projects.models import Project
from placements.models import Company, JobPosting, Application


class Command(BaseCommand):
    help = "Seed the database with demo data so the full workflow can be explored immediately."

    def handle(self, *args, **options):
        if User.objects.filter(username='admin').exists():
            self.stdout.write(self.style.WARNING("Demo data already present — skipping. Delete db.sqlite3 to reseed."))
            return

        today = timezone.localdate()

        admin = User.objects.create_superuser('admin', 'admin@trackpoint.local', 'Admin@123',
                                               first_name='Admin', role=User.Role.ADMIN)
        trainer1 = User.objects.create_user('trainer1', 'trainer1@trackpoint.local', 'Trainer@123',
                                             first_name='Kavya', last_name='Patil', role=User.Role.TRAINER)
        trainer2 = User.objects.create_user('trainer2', 'trainer2@trackpoint.local', 'Trainer@123',
                                             first_name='Rohit', last_name='Sharma', role=User.Role.TRAINER)

        course_py = Course.objects.create(name='Python Full Stack Development', duration_weeks=12,
                                           description='Django, REST APIs, and frontend fundamentals.')
        course_java = Course.objects.create(name='Java Full Stack Development', duration_weeks=14,
                                             description='Core Java, Spring Boot, and SQL.')

        batch1 = Batch.objects.create(name='PFS-Morning-Oct26', course=course_py, trainer=trainer1,
                                       timing='Mon-Fri, 9:00 AM - 12:00 PM',
                                       start_date=today - datetime.timedelta(days=20), status=Batch.Status.ONGOING,
                                       max_students=25)
        batch2 = Batch.objects.create(name='JFS-Evening-Oct26', course=course_java, trainer=trainer2,
                                       timing='Mon-Fri, 6:00 PM - 9:00 PM',
                                       start_date=today + datetime.timedelta(days=10), status=Batch.Status.UPCOMING,
                                       max_students=20)

        student_names = [
            ('Aarav', 'Deshmukh'), ('Ananya', 'Kulkarni'), ('Rohan', 'Joshi'), ('Sneha', 'Patil'),
            ('Vikram', 'Naik'), ('Priya', 'Hegde'), ('Arjun', 'Bhat'), ('Isha', 'Gowda'),
            ('Kiran', 'Malli'), ('Meera', 'Shetty'),
        ]
        students = []
        for idx, (first, last) in enumerate(student_names):
            batch = batch1 if idx < 7 else batch2
            course = course_py if batch == batch1 else course_java
            status = Student.Status.ACTIVE
            if idx == 8:
                status = Student.Status.PLACED
            s = Student.objects.create(
                first_name=first, last_name=last,
                email=f"{first.lower()}.{last.lower()}@example.com",
                phone=f"98{idx:08d}", course=course, batch=batch, status=status,
                gender=Student.Gender.MALE if idx % 2 == 0 else Student.Gender.FEMALE,
            )
            students.append(s)

        batch1_students = students[:7]
        for day_offset in range(5, 0, -1):
            d = today - datetime.timedelta(days=day_offset)
            if d.weekday() >= 5:
                continue
            for i, s in enumerate(batch1_students):
                status = Attendance.Status.ABSENT if (i + day_offset) % 5 == 0 else Attendance.Status.PRESENT
                Attendance.objects.create(student=s, batch=batch1, date=d, status=status, marked_by=trainer1)

        test = MockTest.objects.create(batch=batch1, topic='Django ORM & REST Basics',
                                        test_date=today - datetime.timedelta(days=3),
                                        test_time=datetime.time(10, 0), total_marks=50, created_by=trainer1)
        for i, s in enumerate(batch1_students):
            MockTestResult.objects.create(test=test, student=s, marks_obtained=32 + (i * 3) % 18)

        upcoming_test = MockTest.objects.create(batch=batch1, topic='REST Framework & Auth',
                                                 test_date=today + datetime.timedelta(days=4),
                                                 test_time=datetime.time(10, 0), total_marks=50, created_by=trainer1)

        MockInterview.objects.create(student=batch1_students[0], batch=batch1,
                                      interview_date=today - datetime.timedelta(days=2),
                                      interview_time=datetime.time(11, 0), interviewer_name='Suresh Rao',
                                      round_type=MockInterview.RoundType.TECHNICAL, attended=True,
                                      feedback='Strong grasp of Django ORM; needs to practice system design.',
                                      score=7, scheduled_by=trainer1)
        MockInterview.objects.create(student=batch1_students[1], batch=batch1,
                                      interview_date=today + datetime.timedelta(days=5),
                                      interview_time=datetime.time(14, 0), interviewer_name='Anita Desai',
                                      round_type=MockInterview.RoundType.HR, scheduled_by=trainer1)

        project = Project.objects.create(title='Library Management System', batch=batch1,
                                          description='A Django app to manage book inventory and lending.',
                                          start_date=today - datetime.timedelta(days=15),
                                          status=Project.Status.IN_PROGRESS)
        project.students.set(batch1_students[:3])

        company = Company.objects.create(name='TechNova Solutions', website='https://technova.example.com',
                                          contact_email='hr@technova.example.com', contact_phone='9880000000')
        job = JobPosting.objects.create(company=company, job_role='Junior Python Developer', job_code='TN-PY-01',
                                         description='Entry-level Django developer role.', ctc_offered=4.5,
                                         eligibility_criteria='Completed Python Full Stack course')
        Application.objects.create(student=students[8], job=job, interview_status=Application.InterviewStatus.COMPLETED,
                                    selection_status=Application.SelectionStatus.SELECTED, offer_ctc=4.5)
        Application.objects.create(student=batch1_students[2], job=job,
                                    interview_status=Application.InterviewStatus.SCHEDULED,
                                    selection_status=Application.SelectionStatus.SHORTLISTED)

        self.stdout.write(self.style.SUCCESS(
            "Demo data created.\n"
            "  Admin login:   admin / Admin@123\n"
            "  Trainer login: trainer1 / Trainer@123 (or trainer2 / Trainer@123)"
        ))
