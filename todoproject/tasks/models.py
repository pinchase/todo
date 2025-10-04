from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid
# Create your models here.


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']




class EmailVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='email_verification')
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    verified_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {'verified' if self.is_verified else 'pending'}"

    def is_expired(self):
        """check if verification link is expired (24 hours)"""
        from datetime import timedelta
        expiry_time = self.created_at + timedelta(hours=24)
        return expiry_time < timezone.now()

    class Meta:
        verbose_name = 'Email Verification'
        verbose_name_plural = 'Email Verifications'
