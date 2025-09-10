from django.db import models
from django.conf import settings
import uuid


class SystemAnalytics(models.Model):
    """Model for storing system-wide analytics data."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    total_users = models.IntegerField(default=0)
    total_applications = models.IntegerField(default=0)
    active_applications = models.IntegerField(default=0)
    applications_this_month = models.IntegerField(default=0)
    applications_this_week = models.IntegerField(default=0)
    top_companies = models.JSONField(default=list)
    status_distribution = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'System Analytics'
        verbose_name_plural = 'System Analytics'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Analytics - {self.created_at.strftime('%Y-%m-%d %H:%M')}"


class UserAnalytics(models.Model):
    """Model for storing user-specific analytics data."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='analytics'
    )
    total_applications = models.IntegerField(default=0)
    applications_this_month = models.IntegerField(default=0)
    applications_this_week = models.IntegerField(default=0)
    status_distribution = models.JSONField(default=dict)
    top_companies = models.JSONField(default=list)
    average_response_time = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'User Analytics'
        verbose_name_plural = 'User Analytics'
        ordering = ['-updated_at']
        unique_together = ['user']
    
    def __str__(self):
        return f"Analytics for {self.user.email}"


class EmailLog(models.Model):
    """Model for tracking email communications."""
    
    EMAIL_TYPES = (
        ('verification', 'Email Verification'),
        ('password_reset', 'Password Reset'),
        ('interview_reminder', 'Interview Reminder'),
        ('weekly_summary', 'Weekly Summary'),
        ('broadcast', 'Broadcast Notification'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='email_logs',
        null=True,
        blank=True
    )
    email_type = models.CharField(max_length=20, choices=EMAIL_TYPES)
    recipient_email = models.EmailField()
    subject = models.CharField(max_length=200)
    sent_at = models.DateTimeField(auto_now_add=True)
    is_sent = models.BooleanField(default=False)
    error_message = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Email Log'
        verbose_name_plural = 'Email Logs'
        ordering = ['-sent_at']
    
    def __str__(self):
        return f"{self.email_type} to {self.recipient_email}" 