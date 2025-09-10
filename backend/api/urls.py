from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # JWT Authentication
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Custom authentication endpoints
    path('auth/', include('apps.accounts.urls')),
    
    # User management endpoints
    path('users/', include('apps.users.urls')),
    
    # Job applications
    path('jobs/', include('apps.jobs.urls')),
    
    # Analytics
    path('analytics/', include('apps.analytics.urls')),
    
    # Admin endpoints
    path('admin/', include('apps.users.admin_urls')),
] 