from django.db import models
from django.contrib.auth import get_user_model
#from userprofile.models import User

User = get_user_model()

# Create your models here.
class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    model_name = models.CharField(max_length=100)
    action = models.CharField(max_length=10)
    details = models.TextField()