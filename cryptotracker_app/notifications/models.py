from django.db import models
from django.contrib.auth.models import User


class Notification(models.Model):
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'Notificação para {self.user.username}'
