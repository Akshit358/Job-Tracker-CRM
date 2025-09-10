from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom token obtain view with additional user data."""
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            # Add user information to response
            user = User.objects.get(email=request.data['email'])
            response.data['user'] = {
                'id': str(user.id),
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.role,
                'is_email_verified': user.is_email_verified,
            }
        
        return response


class LogoutView(APIView):
    """View for user logout."""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            
            return Response({
                'message': 'Successfully logged out.'
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
                'error': 'Invalid token.'
            }, status=status.HTTP_400_BAD_REQUEST)


class CheckAuthView(APIView):
    """View for checking authentication status."""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        return Response({
            'user': {
                'id': str(user.id),
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.role,
                'is_email_verified': user.is_email_verified,
            },
            'is_authenticated': True
        }, status=status.HTTP_200_OK) 