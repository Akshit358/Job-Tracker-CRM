from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.CustomTokenObtainPairView.as_view(), name='auth-login'),
    path('logout/', views.LogoutView.as_view(), name='auth-logout'),
    path('check/', views.CheckAuthView.as_view(), name='auth-check'),
] 