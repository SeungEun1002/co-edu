from django.db import models
from user.models import User, Mentor

class MentoringRequest(models.Model):
    STATUS_CHOICES = (
        ('ong', '요청 중'),
        ('act', '요청 수락'),
        ('cle', '요청 취소'),
        ('rej', '요청 거절'),
    )

    mentee = models.ForeignKey(User, on_delete=models.CASCADE)
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    created_datetime = models.DateTimeField(auto_now_add=True)
    mentoring_subject = models.TextField()
    mentoring_timetable = models.ForeignKey('MentoringTimeTable', on_delete=models.CASCADE)
    status = models.CharField(max_length=5, choices=STATUS_CHOICES)

class MentoringTimeTable(models.Model):
    STATUS_CHOICES = (
        ('ini', '멘토링 가능'),
        ('ong', '멘토링 진행 중'),
        ('cpt', '멘토링 완료'),
        ('unc', '멘토링 미완료'),
    )

    start_datetime = models.DateTimeField()
    mentee = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    mentoring_subject = models.TextField(null=True, blank=True)
    before_memo = models.TextField(null=True, blank=True)
    after_memo = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=5, choices=STATUS_CHOICES)
