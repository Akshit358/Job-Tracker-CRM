from django.db import models
from django.conf import settings
import uuid


class JobApplication(models.Model):
    """Model for tracking job applications."""
    
    STATUS_CHOICES = (
        ('applied', 'Applied'),
        ('interviewing', 'Interviewing'),
        ('offer', 'Offer'),
        ('rejected', 'Rejected'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='job_applications'
    )
    company_name = models.CharField(max_length=200)
    job_title = models.CharField(max_length=200)
    application_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    notes = models.TextField(blank=True)
    resume_url = models.URLField(blank=True, max_length=500)
    interview_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Job Application'
        verbose_name_plural = 'Job Applications'
        ordering = ['-application_date', '-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['company_name']),
            models.Index(fields=['application_date']),
        ]
    
    def __str__(self):
        return f"{self.job_title} at {self.company_name}"
    
    @property
    def days_since_applied(self):
        """Calculate days since application was submitted."""
        from django.utils import timezone
        return (timezone.now().date() - self.application_date).days
    
    @property
    def status_display(self):
        """Get the display name for the status."""
        return dict(self.STATUS_CHOICES).get(self.status, self.status)
    
    def get_status_color(self):
        """Get color class for status display."""
        status_colors = {
            'applied': 'blue',
            'interviewing': 'yellow',
            'offer': 'green',
            'rejected': 'red',
        }
        return status_colors.get(self.status, 'gray')


class ApplicationActivity(models.Model):
    """Model for tracking activity on job applications."""
    
    ACTIVITY_TYPES = (
        ('status_change', 'Status Change'),
        ('note_added', 'Note Added'),
        ('interview_scheduled', 'Interview Scheduled'),
        ('reminder_sent', 'Reminder Sent'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job_application = models.ForeignKey(
        JobApplication,
        on_delete=models.CASCADE,
        related_name='activities'
    )
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Application Activity'
        verbose_name_plural = 'Application Activities'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_activity_type_display()} - {self.job_application}" 