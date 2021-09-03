from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime

class Subject(models.Model):
    code = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=50)

class User(AbstractUser):
    YEAR_CHOICES = [(r, r) for r in range(2000, datetime.date.today().year+1)]
    GENDER_CHOICES = (
        ('man', '남'),
        ('wom', '여'),
    )

    name = models.CharField(max_length=50)
    university = models.CharField(max_length=50)
    admission_year = models.CharField(max_length=6, choices=YEAR_CHOICES)
    gender = models.CharField(max_length=5, choices=GENDER_CHOICES)
    interest_subject = models.TextField()
    is_mentor = models.BooleanField(default=False)

class Mentor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    major = models.CharField(max_length=50)
    subject = models.ManyToManyField(Subject)
    teaching_subject = models.TextField()
    introduction = models.TextField()
    service_hour = models.PositiveIntegerField(default=0)