"""
Views for the API user
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework import serializers

from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
)


class CreateUserView(generics.CreateAPIView):
    """Creating a new user in the system"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user


class EmptySerializer(serializers.Serializer):
    """Serializer for logout request (does not accept any input)"""
    pass


class LogoutView(APIView):
    """Log out user by deleting the token"""
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EmptySerializer  # ✅ Added serializer to avoid DRF warnings

    def post(self, request):
        """Handle user logout by deleting the authentication token"""
        request.user.auth_token.delete()
        return Response({"message": "Logged out successfully"})
