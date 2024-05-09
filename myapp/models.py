from django.db import models

from django.contrib.auth.models import User

class Notification(models.Model):
    title = models.CharField(max_length=100)
    message = models.TextField()
    notification_type = models.CharField(max_length=50, choices=[('info', 'Info'), ('warning', 'Warning'), ('error', 'Error')])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
