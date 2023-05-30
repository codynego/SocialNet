from django.db import models
from userprofile.models import User

# Create your models here.

class Notification(models.Model):
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notify')
    message = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)