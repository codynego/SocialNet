from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken

# Create your models here.

class User(AbstractUser):
    GENDER_CHOICES = (
        ('m', 'male'),
        ('f', 'female'),
        ('O', 'Other'),
    )

    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    profile_pics = models.ImageField(upload_to='img', null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    followers = models.ManyToManyField('self', related_name='following', symmetrical=False, blank=True)

    def __str__(self):
        return self.username
    
    def get_fullname(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    def get_token(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }