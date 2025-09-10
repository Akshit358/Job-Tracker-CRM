from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='user-register'),
    path('verify-email/', views.EmailVerificationView.as_view(), name='email-verify'),
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('update/', views.UserUpdateView.as_view(), name='user-update'),
    path('change-password/', views.PasswordChangeView.as_view(), name='password-change'),
    path('reset-password/', views.PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('reset-password/confirm/', views.PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
] 