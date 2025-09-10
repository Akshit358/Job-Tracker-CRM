from rest_framework import status, generics, permissions, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q
from datetime import datetime, timedelta

from .models import JobApplication, ApplicationActivity
from .serializers import (
    JobApplicationSerializer,
    JobApplicationCreateSerializer,
    JobApplicationUpdateSerializer,
    ApplicationActivitySerializer,
    JobApplicationFilter,
)


class JobApplicationViewSet(viewsets.ModelViewSet):
    """ViewSet for JobApplication CRUD operations."""
    
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = JobApplicationFilter
    
    def get_queryset(self):
        """Return job applications for the current user."""
        return JobApplication.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'create':
            return JobApplicationCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return JobApplicationUpdateSerializer
        return JobApplicationSerializer
    
    def perform_create(self, serializer):
        """Create job application and log activity."""
        job_application = serializer.save()
        
        # Create initial activity log
        ApplicationActivity.objects.create(
            job_application=job_application,
            activity_type='status_change',
            description=f'Application created with status: {job_application.get_status_display()}'
        )
    
    @action(detail=True, methods=['get'])
    def activities(self, request, pk=None):
        """Get activities for a specific job application."""
        job_application = self.get_object()
        activities = ApplicationActivity.objects.filter(job_application=job_application)
        serializer = ApplicationActivitySerializer(activities, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get user's job application statistics."""
        user = request.user
        queryset = self.get_queryset()
        
        # Basic counts
        total_applications = queryset.count()
        applications_this_month = queryset.filter(
            application_date__gte=datetime.now().replace(day=1)
        ).count()
        applications_this_week = queryset.filter(
            application_date__gte=datetime.now() - timedelta(days=7)
        ).count()
        
        # Status distribution
        status_distribution = queryset.values('status').annotate(
            count=Count('status')
        ).order_by('status')
        
        # Top companies
        top_companies = queryset.values('company_name').annotate(
            count=Count('company_name')
        ).order_by('-count')[:5]
        
        # Recent applications
        recent_applications = queryset.order_by('-created_at')[:5]
        
        return Response({
            'total_applications': total_applications,
            'applications_this_month': applications_this_month,
            'applications_this_week': applications_this_week,
            'status_distribution': list(status_distribution),
            'top_companies': list(top_companies),
            'recent_applications': JobApplicationSerializer(recent_applications, many=True).data
        })
    
    @action(detail=False, methods=['get'])
    def timeline(self, request):
        """Get user's application timeline."""
        queryset = self.get_queryset()
        
        # Get applications grouped by month
        timeline_data = queryset.extra(
            select={'month': "EXTRACT(month FROM application_date)"}
        ).values('month').annotate(
            count=Count('id')
        ).order_by('month')
        
        return Response({
            'timeline': list(timeline_data)
        })


class ApplicationActivityViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for ApplicationActivity (read-only)."""
    
    serializer_class = ApplicationActivitySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return activities for the current user's applications."""
        return ApplicationActivity.objects.filter(
            job_application__user=self.request.user
        )


class JobApplicationSearchView(generics.ListAPIView):
    """View for searching job applications."""
    
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return filtered job applications based on search parameters."""
        queryset = JobApplication.objects.filter(user=self.request.user)
        
        # Search by company name
        company = self.request.query_params.get('company', None)
        if company:
            queryset = queryset.filter(company_name__icontains=company)
        
        # Search by job title
        job_title = self.request.query_params.get('job_title', None)
        if job_title:
            queryset = queryset.filter(job_title__icontains=job_title)
        
        # Filter by status
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            status_list = status_filter.split(',')
            queryset = queryset.filter(status__in=status_list)
        
        # Filter by date range
        date_from = self.request.query_params.get('date_from', None)
        if date_from:
            queryset = queryset.filter(application_date__gte=date_from)
        
        date_to = self.request.query_params.get('date_to', None)
        if date_to:
            queryset = queryset.filter(application_date__lte=date_to)
        
        return queryset.order_by('-application_date') 