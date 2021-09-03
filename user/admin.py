from django.contrib import admin
from .models import *


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['code', 'name']

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'name']
    list_filter = ['is_active']
    search_fields = ['username']

@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    list_display = ['user', 'major']
