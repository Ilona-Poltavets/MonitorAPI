from django.db import models
from django.contrib.auth.models import User


class Device(models.Model):
    user = models.ForeignKey(User, related_name='devices', on_delete=models.CASCADE)
    device_name = models.CharField(max_length=255)
    cpu = models.CharField(max_length=255)
    gpu = models.CharField(max_length=255)
    ram = models.CharField(max_length=255)
    os = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.device_name} ({self.user.username})"


class ChatMessage(models.Model):
    user_message = models.TextField()
    gpt_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.timestamp}"
