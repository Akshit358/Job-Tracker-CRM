from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'system', views.SystemAnalyticsViewSet, basename='system-analytics')
router.register(r'user', views.UserAnalyticsViewSet, basename='user-analytics')
router.register(r'emails', views.EmailLogViewSet, basename='email-logs')

urlpatterns = [
    path('', include(router.urls)),
] 