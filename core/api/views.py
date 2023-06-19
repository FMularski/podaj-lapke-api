"""
    API views of the core app.
"""
from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.api import serializers

User = get_user_model()


class UserRegisterAPIView(generics.CreateAPIView):
    """Register an user with username, email and password."""

    serializer_class = serializers.UserRegisterSerializer
    queryset = User.objects.all()


class UserMeApiView(generics.RetrieveUpdateAPIView):
    """Get user details."""

    serializer_class = serializers.UserSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class ChangePasswordApiView(generics.UpdateAPIView):
    """Update user password."""

    serializer_class = serializers.ChangePasswordSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    http_method_names = ("put",)

    def get_object(self):
        return self.request.user
