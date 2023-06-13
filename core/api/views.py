"""
    API views of the core app.
"""
from django.contrib.auth import get_user_model
from rest_framework import generics

from core.api import serializers

User = get_user_model()


class UserRegisterAPIView(generics.CreateAPIView):
    """Register an user with username, email and password."""

    serializer_class = serializers.UserRegisterSerializer
    queryset = User.objects.all()
