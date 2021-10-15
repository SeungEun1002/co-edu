from django.contrib import admin
from .models import *

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'content', 'created_datetime']
