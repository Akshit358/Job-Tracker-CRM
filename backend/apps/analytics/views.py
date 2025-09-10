from rest_framework import status, generics, permissions, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Count, Q, Avg
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model

from .models import SystemAnalytics, UserAnalytics, EmailLog
from .serializers import (
    SystemAnalyticsSerializer,
    UserAnalyticsSerializer,
    EmailLogSerializer,
)
from apps.jobs.models import JobApplication

User = get_user_model()


class AnalyticsPermission(permissions.BasePermission):
    """Custom permission for analytics access."""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class SystemAnalyticsViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for system-wide analytics."""
    
    serializer_class = SystemAnalyticsSerializer
    permission_classes = [AnalyticsPermission]
    queryset = SystemAnalytics.objects.all()
    
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """Get comprehensive system dashboard data."""
        
        # User statistics
        total_users = User.objects.count()
        active_users = User.objects.filter(is_active=True).count()
        verified_users = User.objects.filter(is_email_verified=True).count()
        new_users_this_month = User.objects.filter(
            date_joined__gte=timezone.now().replace(day=1)
        ).count()
        
        # Job application statistics
        total_applications = JobApplication.objects.count()
        applications_this_month = JobApplication.objects.filter(
            application_date__gte=timezone.now().replace(day=1)
        ).count()
        applications_this_week = JobApplication.objects.filter(
            application_date__gte=timezone.now() - timedelta(days=7)
        ).count()
        
        # Status distribution
        status_distribution = JobApplication.objects.values('status').annotate(
            count=Count('status')
        ).order_by('status')
        
        # Top companies
        top_companies = JobApplication.objects.values('company_name').annotate(
            count=Count('company_name')
        ).order_by('-count')[:10]
        
        # Monthly trends (last 6 months)
        monthly_trends = []
        for i in range(6):
            month_start = timezone.now().replace(day=1) - timedelta(days=30*i)
            month_end = month_start.replace(day=28) + timedelta(days=4)
            month_end = month_end.replace(day=1) - timedelta(days=1)
            
            count = JobApplication.objects.filter(
                application_date__gte=month_start,
                application_date__lte=month_end
            ).count()
            
            monthly_trends.append({
                'month': month_start.strftime('%Y-%m'),
                'count': count
            })
        
        # Recent activity
        recent_applications = JobApplication.objects.select_related('user').order_by('-created_at')[:10]
        
        return Response({
            'users': {
                'total': total_users,
                'active': active_users,
                'verified': verified_users,
                'new_this_month': new_users_this_month,
            },
            'applications': {
                'total': total_applications,
                'this_month': applications_this_month,
                'this_week': applications_this_week,
            },
            'status_distribution': list(status_distribution),
            'top_companies': list(top_companies),
            'monthly_trends': monthly_trends,
            'recent_applications': [
                {
                    'id': app.id,
                    'company_name': app.company_name,
                    'job_title': app.job_title,
                    'status': app.status,
                    'user_email': app.user.email,
                    'created_at': app.created_at,
                }
                for app in recent_applications
            ]
        })


class UserAnalyticsViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for user-specific analytics."""
    
    serializer_class = UserAnalyticsSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return analytics for the current user."""
        return UserAnalytics.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """Get user's analytics dashboard."""
        user = request.user
        
        # Get user's job applications
        applications = JobApplication.objects.filter(user=user)
        
        # Basic statistics
        total_applications = applications.count()
        applications_this_month = applications.filter(
            application_date__gte=timezone.now().replace(day=1)
        ).count()
        applications_this_week = applications.filter(
            application_date__gte=timezone.now() - timedelta(days=7)
        ).count()
        
        # Status distribution
        status_distribution = applications.values('status').annotate(
            count=Count('status')
        ).order_by('status')
        
        # Top companies
        top_companies = applications.values('company_name').annotate(
            count=Count('company_name')
        ).order_by('-count')[:5]
        
        # Average response time (days between application and status change)
        response_times = []
        for app in applications.filter(status__in=['interviewing', 'offer', 'rejected']):
            if app.updated_at and app.created_at:
                days = (app.updated_at.date() - app.application_date).days
                if days > 0:
                    response_times.append(days)
        
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        
        # Monthly activity
        monthly_activity = []
        for i in range(6):
            month_start = timezone.now().replace(day=1) - timedelta(days=30*i)
            month_end = month_start.replace(day=28) + timedelta(days=4)
            month_end = month_end.replace(day=1) - timedelta(days=1)
            
            count = applications.filter(
                application_date__gte=month_start,
                application_date__lte=month_end
            ).count()
            
            monthly_activity.append({
                'month': month_start.strftime('%Y-%m'),
                'count': count
            })
        
        return Response({
            'total_applications': total_applications,
            'applications_this_month': applications_this_month,
            'applications_this_week': applications_this_week,
            'status_distribution': list(status_distribution),
            'top_companies': list(top_companies),
            'average_response_time': round(avg_response_time, 1),
            'monthly_activity': monthly_activity,
        })


class EmailLogViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for email logs."""
    
    serializer_class = EmailLogSerializer
    permission_classes = [AnalyticsPermission]
    queryset = EmailLog.objects.all()
    
    def get_queryset(self):
        """Filter email logs based on user permissions."""
        if self.request.user.is_admin:
            return EmailLog.objects.all()
        return EmailLog.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get email statistics."""
        queryset = self.get_queryset()
        
        # Email type distribution
        type_distribution = queryset.values('email_type').annotate(
            count=Count('email_type')
        ).order_by('email_type')
        
        # Success rate
        total_emails = queryset.count()
        successful_emails = queryset.filter(is_sent=True).count()
        success_rate = (successful_emails / total_emails * 100) if total_emails > 0 else 0
        
        # Recent emails
        recent_emails = queryset.order_by('-sent_at')[:10]
        
        return Response({
            'type_distribution': list(type_distribution),
            'total_emails': total_emails,
            'successful_emails': successful_emails,
            'success_rate': round(success_rate, 2),
            'recent_emails': EmailLogSerializer(recent_emails, many=True).data
        }) 