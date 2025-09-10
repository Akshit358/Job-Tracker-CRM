from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .models import JobApplication
from apps.analytics.models import EmailLog


@shared_task
def send_interview_reminder():
    """Send interview reminders 24 hours before scheduled interviews."""
    
    tomorrow = timezone.now() + timedelta(days=1)
    applications = JobApplication.objects.filter(
        interview_date__date=tomorrow.date(),
        status='interviewing'
    ).select_related('user')
    
    for application in applications:
        try:
            subject = f'Interview Reminder: {application.job_title} at {application.company_name}'
            message = f"""
            Hello {application.user.first_name},
            
            This is a reminder that you have an interview tomorrow for the position of {application.job_title} at {application.company_name}.
            
            Interview Details:
            - Date: {application.interview_date.strftime('%B %d, %Y at %I:%M %p')}
            - Position: {application.job_title}
            - Company: {application.company_name}
            
            Good luck with your interview!
            
            Best regards,
            Job Tracker Team
            """
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [application.user.email],
                fail_silently=False,
            )
            
            # Log the email
            EmailLog.objects.create(
                user=application.user,
                email_type='interview_reminder',
                recipient_email=application.user.email,
                subject=subject,
                is_sent=True
            )
            
        except Exception as e:
            # Log failed email
            EmailLog.objects.create(
                user=application.user,
                email_type='interview_reminder',
                recipient_email=application.user.email,
                subject=subject,
                is_sent=False,
                error_message=str(e)
            )


@shared_task
def send_weekly_summary():
    """Send weekly summary emails to users."""
    
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    users = User.objects.filter(is_active=True, is_email_verified=True)
    
    for user in users:
        try:
            # Get user's applications for the past week
            week_ago = timezone.now() - timedelta(days=7)
            applications = JobApplication.objects.filter(
                user=user,
                created_at__gte=week_ago
            )
            
            if applications.exists():
                subject = 'Your Weekly Job Application Summary'
                message = f"""
                Hello {user.first_name},
                
                Here's your weekly job application summary:
                
                New Applications This Week: {applications.count()}
                
                Recent Applications:
                """
                
                for app in applications[:5]:
                    message += f"- {app.job_title} at {app.company_name} ({app.status})\n"
                
                message += """
                
                Keep up the great work!
                
                Best regards,
                Job Tracker Team
                """
                
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
                
                # Log the email
                EmailLog.objects.create(
                    user=user,
                    email_type='weekly_summary',
                    recipient_email=user.email,
                    subject=subject,
                    is_sent=True
                )
                
        except Exception as e:
            # Log failed email
            EmailLog.objects.create(
                user=user,
                email_type='weekly_summary',
                recipient_email=user.email,
                subject=subject,
                is_sent=False,
                error_message=str(e)
            )


@shared_task
def update_analytics():
    """Update system and user analytics."""
    
    from apps.analytics.models import SystemAnalytics, UserAnalytics
    from django.contrib.auth import get_user_model
    from django.db.models import Count
    from datetime import datetime
    
    User = get_user_model()
    
    # Update system analytics
    total_users = User.objects.count()
    total_applications = JobApplication.objects.count()
    active_applications = JobApplication.objects.filter(status__in=['applied', 'interviewing']).count()
    
    applications_this_month = JobApplication.objects.filter(
        application_date__gte=datetime.now().replace(day=1)
    ).count()
    
    applications_this_week = JobApplication.objects.filter(
        application_date__gte=timezone.now() - timedelta(days=7)
    ).count()
    
    # Get top companies
    top_companies = list(JobApplication.objects.values('company_name').annotate(
        count=Count('company_name')
    ).order_by('-count')[:10])
    
    # Get status distribution
    status_distribution = dict(JobApplication.objects.values('status').annotate(
        count=Count('status')
    ).values_list('status', 'count'))
    
    # Create or update system analytics
    SystemAnalytics.objects.create(
        total_users=total_users,
        total_applications=total_applications,
        active_applications=active_applications,
        applications_this_month=applications_this_month,
        applications_this_week=applications_this_week,
        top_companies=top_companies,
        status_distribution=status_distribution
    )
    
    # Update user analytics
    for user in User.objects.filter(is_active=True):
        user_applications = JobApplication.objects.filter(user=user)
        
        user_analytics, created = UserAnalytics.objects.get_or_create(user=user)
        
        user_analytics.total_applications = user_applications.count()
        user_analytics.applications_this_month = user_applications.filter(
            application_date__gte=datetime.now().replace(day=1)
        ).count()
        user_analytics.applications_this_week = user_applications.filter(
            application_date__gte=timezone.now() - timedelta(days=7)
        ).count()
        
        # Get user's status distribution
        user_status_distribution = dict(user_applications.values('status').annotate(
            count=Count('status')
        ).values_list('status', 'count'))
        
        # Get user's top companies
        user_top_companies = list(user_applications.values('company_name').annotate(
            count=Count('company_name')
        ).order_by('-count')[:5])
        
        user_analytics.status_distribution = user_status_distribution
        user_analytics.top_companies = user_top_companies
        user_analytics.save() 