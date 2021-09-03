from django.contrib import admin
from .models import *

@admin.register(MentoringRequest)
class MentoringRequestAdmin(admin.ModelAdmin):
    list_display = ['mentee', 'mentor', 'mentoring_timetable', 'status']

@admin.register(MentoringTimeTable)
class MentoringTimeTableAdmin(admin.ModelAdmin):
    list_display = ['mentor', 'mentee', 'start_datetime', 'status']

