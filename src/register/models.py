from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    device_token = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True, null=True, unique=True)
    user_type = models.CharField(max_length=10, choices=[("Creative", "creative"), ("Investor", "investor")], default="creative")
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='idea_photos/', null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.user.username


class PasswordRestCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)
    reset_code = models.CharField(max_length=6, null=True, blank=True)
    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=10)