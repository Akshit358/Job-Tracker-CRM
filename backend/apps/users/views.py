from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.db import transaction
import uuid

from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    UserUpdateSerializer,
    PasswordChangeSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    EmailVerificationSerializer,
)

User = get_user_model()


class UserRegistrationView(APIView):
    """View for user registration with email verification."""
    
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                user = serializer.save()
                
                # Send email verification
                self.send_verification_email(user)
                
                return Response({
                    'message': 'User registered successfully. Please check your email for verification.',
                    'user_id': user.id
                }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def send_verification_email(self, user):
        """Send email verification to user."""
        subject = 'Verify your email address'
        message = f"""
        Hello {user.first_name},
        
        Please verify your email address by clicking the link below:
        
        {settings.FRONTEND_URL}/verify-email?token={user.email_verification_token}
        
        If you didn't create an account, please ignore this email.
        
        Best regards,
        Job Tracker Team
        """
        
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
        except Exception as e:
            # Log the error but don't fail the registration
            print(f"Failed to send verification email: {e}")


class EmailVerificationView(APIView):
    """View for email verification."""
    
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = EmailVerificationSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data['token']
            
            try:
                user = User.objects.get(email_verification_token=token, is_email_verified=False)
                user.is_email_verified = True
                user.email_verification_token = uuid.uuid4()
                user.save()
                
                return Response({
                    'message': 'Email verified successfully.'
                }, status=status.HTTP_200_OK)
            
            except User.DoesNotExist:
                return Response({
                    'error': 'Invalid or expired verification token.'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """View for user profile management."""
    
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class UserUpdateView(generics.UpdateAPIView):
    """View for updating user profile."""
    
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class PasswordChangeView(APIView):
    """View for changing user password."""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            return Response({
                'message': 'Password changed successfully.'
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestView(APIView):
    """View for requesting password reset."""
    
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            
            try:
                user = User.objects.get(email=email, is_active=True)
                # Generate reset token
                reset_token = uuid.uuid4()
                user.email_verification_token = reset_token
                user.save()
                
                # Send reset email
                self.send_reset_email(user, reset_token)
                
                return Response({
                    'message': 'Password reset email sent successfully.'
                }, status=status.HTTP_200_OK)
            
            except User.DoesNotExist:
                # Don't reveal if user exists or not
                return Response({
                    'message': 'If an account with this email exists, a password reset email has been sent.'
                }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def send_reset_email(self, user, token):
        """Send password reset email."""
        subject = 'Reset your password'
        message = f"""
        Hello {user.first_name},
        
        You requested a password reset. Click the link below to reset your password:
        
        {settings.FRONTEND_URL}/reset-password?token={token}
        
        If you didn't request this, please ignore this email.
        
        Best regards,
        Job Tracker Team
        """
        
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Failed to send reset email: {e}")


class PasswordResetConfirmView(APIView):
    """View for confirming password reset."""
    
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data['token']
            new_password = serializer.validated_data['new_password']
            
            try:
                user = User.objects.get(email_verification_token=token, is_active=True)
                user.set_password(new_password)
                user.email_verification_token = uuid.uuid4()
                user.save()
                
                return Response({
                    'message': 'Password reset successfully.'
                }, status=status.HTTP_200_OK)
            
            except User.DoesNotExist:
                return Response({
                    'error': 'Invalid or expired reset token.'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 