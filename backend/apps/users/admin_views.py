from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q
from datetime import datetime, timedelta

from .serializers import UserSerializer
from apps.jobs.models import JobApplication
from apps.analytics.models import SystemAnalytics

User = get_user_model()


class AdminPermission(permissions.BasePermission):
    """Custom permission for admin access."""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class AdminUserListView(generics.ListAPIView):
    """Admin view for listing all users."""
    
    serializer_class = UserSerializer
    permission_classes = [AdminPermission]
    queryset = User.objects.all()
    
    def get_queryset(self):
        queryset = User.objects.all()
        
        # Filter by role
        role = self.request.query_params.get('role', None)
        if role:
            queryset = queryset.filter(role=role)
        
        # Filter by email verification status
        is_verified = self.request.query_params.get('is_verified', None)
        if is_verified is not None:
            is_verified = is_verified.lower() == 'true'
            queryset = queryset.filter(is_email_verified=is_verified)
        
        # Filter by active status
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            is_active = is_active.lower() == 'true'
            queryset = queryset.filter(is_active=is_active)
        
        # Search by name or email
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search)
            )
        
        return queryset.order_by('-created_at')


class AdminUserDetailView(generics.RetrieveAPIView):
    """Admin view for user details."""
    
    serializer_class = UserSerializer
    permission_classes = [AdminPermission]
    queryset = User.objects.all()
    lookup_field = 'pk'


class AdminUserDeactivateView(APIView):
    """Admin view for deactivating a user."""
    
    permission_classes = [AdminPermission]
    
    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        
        if user == request.user:
            return Response({
                'error': 'You cannot deactivate your own account.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user.is_active = False
        user.save()
        
        return Response({
            'message': f'User {user.email} has been deactivated.'
        }, status=status.HTTP_200_OK)


class AdminUserActivateView(APIView):
    """Admin view for activating a user."""
    
    permission_classes = [AdminPermission]
    
    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.is_active = True
        user.save()
        
        return Response({
            'message': f'User {user.email} has been activated.'
        }, status=status.HTTP_200_OK)


class AdminUserDeleteView(APIView):
    """Admin view for deleting a user."""
    
    permission_classes = [AdminPermission]
    
    def delete(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        
        if user == request.user:
            return Response({
                'error': 'You cannot delete your own account.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user.delete()
        
        return Response({
            'message': f'User {user.email} has been deleted.'
        }, status=status.HTTP_200_OK)


class BroadcastNotificationView(APIView):
    """Admin view for sending broadcast notifications."""
    
    permission_classes = [AdminPermission]
    
    def post(self, request):
        subject = request.data.get('subject')
        message = request.data.get('message')
        
        if not subject or not message:
            return Response({
                'error': 'Subject and message are required.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get all active users
        users = User.objects.filter(is_active=True, is_email_verified=True)
        
        success_count = 0
        failed_count = 0
        
        for user in users:
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
                success_count += 1
            except Exception as e:
                failed_count += 1
                print(f"Failed to send broadcast email to {user.email}: {e}")
        
        return Response({
            'message': f'Broadcast sent successfully. {success_count} emails sent, {failed_count} failed.',
            'success_count': success_count,
            'failed_count': failed_count
        }, status=status.HTTP_200_OK)


class AdminDashboardView(APIView):
    """Admin view for dashboard statistics."""
    
    permission_classes = [AdminPermission]
    
    def get(self, request):
        # Get basic statistics
        total_users = User.objects.count()
        active_users = User.objects.filter(is_active=True).count()
        verified_users = User.objects.filter(is_email_verified=True).count()
        
        # Get job application statistics
        total_applications = JobApplication.objects.count()
        applications_this_month = JobApplication.objects.filter(
            application_date__gte=datetime.now().replace(day=1)
        ).count()
        applications_this_week = JobApplication.objects.filter(
            application_date__gte=datetime.now() - timedelta(days=7)
        ).count()
        
        # Get status distribution
        status_distribution = JobApplication.objects.values('status').annotate(
            count=Count('status')
        ).order_by('status')
        
        # Get top companies
        top_companies = JobApplication.objects.values('company_name').annotate(
            count=Count('company_name')
        ).order_by('-count')[:10]
        
        # Get recent activity
        recent_applications = JobApplication.objects.select_related('user').order_by('-created_at')[:10]
        
        return Response({
            'users': {
                'total': total_users,
                'active': active_users,
                'verified': verified_users,
            },
            'applications': {
                'total': total_applications,
                'this_month': applications_this_month,
                'this_week': applications_this_week,
            },
            'status_distribution': list(status_distribution),
            'top_companies': list(top_companies),
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
        }, status=status.HTTP_200_OK) 