from django.contrib import admin
from .models import JobApplication, ApplicationActivity


class ApplicationActivityInline(admin.TabularInline):
    """Inline admin for ApplicationActivity."""
    model = ApplicationActivity
    extra = 0
    readonly_fields = ('created_at',)
    fields = ('activity_type', 'description', 'created_at')


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    """Admin configuration for JobApplication model."""
    
    list_display = ('job_title', 'company_name', 'user', 'status', 'application_date', 'days_since_applied')
    list_filter = ('status', 'application_date', 'created_at', 'user')
    search_fields = ('job_title', 'company_name', 'user__email', 'user__first_name', 'user__last_name')
    ordering = ('-application_date', '-created_at')
    readonly_fields = ('created_at', 'updated_at', 'days_since_applied')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'company_name', 'job_title', 'application_date')
        }),
        ('Status & Details', {
            'fields': ('status', 'notes', 'resume_url', 'interview_date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [ApplicationActivityInline]
    
    def days_since_applied(self, obj):
        return obj.days_since_applied
    days_since_applied.short_description = 'Days Since Applied'


@admin.register(ApplicationActivity)
class ApplicationActivityAdmin(admin.ModelAdmin):
    """Admin configuration for ApplicationActivity model."""
    
    list_display = ('job_application', 'activity_type', 'description', 'created_at')
    list_filter = ('activity_type', 'created_at')
    search_fields = ('job_application__job_title', 'job_application__company_name', 'description')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',) 