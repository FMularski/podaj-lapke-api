"""
    Serializers for models of the core app.
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
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


class ChangePasswordSerializer(serializers.Serializer):
    old = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate_old(self, value):
        user = self.context["request"].user

        if not check_password(value, user.password):
            raise ValidationError("Invalid old password.")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise ValidationError("Password must be at least 8 characters long.")

        if value.islower():
            raise ValidationError("Password must contain at least 1 upper case letter.")

        has_digit = any([char.isdigit() for char in value])
        if not has_digit:
            raise ValidationError("Password must contain at least 1 digit.")

        has_special = any([not char.isalnum() for char in value])
        if not has_special:
            raise ValidationError("Password must contain at least 1 special symbol.")

        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data.get("password"))
        instance.save()

        return instance
