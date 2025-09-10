from rest_framework import serializers
from django_filters import rest_framework as filters
from .models import JobApplication, ApplicationActivity


class JobApplicationSerializer(serializers.ModelSerializer):
    """Serializer for JobApplication model."""
    
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    days_since_applied = serializers.IntegerField(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = JobApplication
        fields = (
            'id', 'user', 'user_email', 'user_name', 'company_name', 'job_title',
            'application_date', 'status', 'status_display', 'notes', 'resume_url',
            'interview_date', 'created_at', 'updated_at', 'days_since_applied'
        )
        read_only_fields = ('id', 'user', 'created_at', 'updated_at', 'days_since_applied')
    
    def create(self, validated_data):
        # Set the user to the current authenticated user
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class JobApplicationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating job applications."""
    
    class Meta:
        model = JobApplication
        fields = (
            'company_name', 'job_title', 'application_date', 'status',
            'notes', 'resume_url', 'interview_date'
        )
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class JobApplicationUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating job applications."""
    
    class Meta:
        model = JobApplication
        fields = (
            'company_name', 'job_title', 'application_date', 'status',
            'notes', 'resume_url', 'interview_date'
        )
    
    def update(self, instance, validated_data):
        # Create activity log for status changes
        if 'status' in validated_data and validated_data['status'] != instance.status:
            ApplicationActivity.objects.create(
                job_application=instance,
                activity_type='status_change',
                description=f'Status changed from {instance.get_status_display()} to {dict(JobApplication.STATUS_CHOICES)[validated_data["status"]]}'
            )
        
        # Create activity log for note updates
        if 'notes' in validated_data and validated_data['notes'] != instance.notes:
            ApplicationActivity.objects.create(
                job_application=instance,
                activity_type='note_added',
                description='Notes updated'
            )
        
        return super().update(instance, validated_data)


class ApplicationActivitySerializer(serializers.ModelSerializer):
    """Serializer for ApplicationActivity model."""
    
    activity_type_display = serializers.CharField(source='get_activity_type_display', read_only=True)
    
    class Meta:
        model = ApplicationActivity
        fields = ('id', 'job_application', 'activity_type', 'activity_type_display', 'description', 'created_at')
        read_only_fields = ('id', 'created_at')


class JobApplicationFilter(filters.FilterSet):
    """Filter for JobApplication model."""
    
    company_name = filters.CharFilter(lookup_expr='icontains')
    job_title = filters.CharFilter(lookup_expr='icontains')
    status = filters.MultipleChoiceFilter(choices=JobApplication.STATUS_CHOICES)
    application_date_from = filters.DateFilter(field_name='application_date', lookup_expr='gte')
    application_date_to = filters.DateFilter(field_name='application_date', lookup_expr='lte')
    created_at_from = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_at_to = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    
    class Meta:
        model = JobApplication
        fields = {
            'company_name': ['exact', 'icontains'],
            'job_title': ['exact', 'icontains'],
            'status': ['exact', 'in'],
            'application_date': ['exact', 'gte', 'lte'],
            'created_at': ['exact', 'gte', 'lte'],
        } 