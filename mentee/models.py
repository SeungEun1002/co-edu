from django.db import models
from user.models import *

class Chat(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_send')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_receive')
    content = models.TextField()
    created_datetime = models.DateTimeField(auto_now_add=True)
