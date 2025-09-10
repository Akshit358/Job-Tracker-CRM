from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'applications', views.JobApplicationViewSet, basename='job-application')
router.register(r'activities', views.ApplicationActivityViewSet, basename='application-activity')

urlpatterns = [
    path('', include(router.urls)),
    path('search/', views.JobApplicationSearchView.as_view(), name='job-search'),
] 