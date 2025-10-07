from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid
# Create your models here.


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    CATEGORY_CHOICES = [
        ('personal', 'Personal'),
        ('work', 'Work'),
        ('school', 'School'),
        ('shopping', 'Shopping'),
        ('travel', 'Travel'),
        ('health', 'Health'),
        ('finance', 'Finance'),
        ('other', 'Other'),
    ]



    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium',
        help_text='Task Priority Level'
    )
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='other',
        help_text='Task Category'
    )

    due_date = models.DateTimeField(null=True, blank=True, help_text='Due Date')

    def __str__(self):
        return self.title

    @property
    def is_overdue(self):
        """Check if task is overdue"""
        if self.due_date and not self.completed:
            return self.due_date < timezone.now()
        return False

    @property
    def due_status(self):
        """Get human-readable due status"""
        if not self.due_date:
            return 'no_deadline'
        if self.completed:
            return 'completed'
        if self.is_overdue:
            return 'overdue'

        time_left = self.due_date - timezone.now()
        if time_left.days == 0:
            return 'due_today'
        elif time_left.days == 1:
            return 'due_tomorrow'
        elif time_left.days <= 7:
            return 'due_this_week'
        else:
            return 'upcoming'

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'completed']),
            models.Index(fields=['user', 'priority']),
            models.Index(fields=['user', 'category']),
            models.Index(fields=['due_date']),
        ]



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


class Subtask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.task.title} - {self.title}"

    class Meta:
        ordering = ['order', 'created_at']