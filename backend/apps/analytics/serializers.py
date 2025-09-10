from rest_framework import serializers
from .models import SystemAnalytics, UserAnalytics, EmailLog


class SystemAnalyticsSerializer(serializers.ModelSerializer):
    """Serializer for SystemAnalytics model."""
    
    class Meta:
        model = SystemAnalytics
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class UserAnalyticsSerializer(serializers.ModelSerializer):
    """Serializer for UserAnalytics model."""
    
    user_email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = UserAnalytics
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class EmailLogSerializer(serializers.ModelSerializer):
    """Serializer for EmailLog model."""
    
    user_email = serializers.EmailField(source='user.email', read_only=True)
    email_type_display = serializers.CharField(source='get_email_type_display', read_only=True)
    
    class Meta:
        model = EmailLog
        fields = '__all__'
        read_only_fields = ('id', 'sent_at') 