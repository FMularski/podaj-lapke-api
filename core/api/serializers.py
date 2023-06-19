"""
    Serializers for models of the core app.
"""
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import ValidationError

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "password",
        )
        read_only_fields = ("id",)
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "notification_push",
            "notification_email",
            "notification_favourites",
            "avatar",
        )
        read_only_fields = "id", "username", "avatar"

    def validate_phone(self, value):
        if not value.isnumeric():
            raise ValidationError("Phone number must contain numbers only.")
        if not len(value) == 9:
            raise ValidationError("Phone number must be exactly 9 digits long.")

        return value
