"""
    Fixtures required for tests of the core app.
"""

import os
import tempfile

import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user():
    """Provides a regular user."""

    def create(
        username="user",
        email="user@example.com",
        password="test123",
        first_name="fname",
        last_name="lname",
        phone="123456789",
        notification_push=False,
        notification_email=False,
        notification_favourites=False,
    ):
        return User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            notification_push=notification_push,
            notification_email=notification_email,
            notification_favourites=notification_favourites,
            avatar=tempfile.NamedTemporaryFile(suffix=".png").name,
        )

    return create


@pytest.fixture
def create_superuser():
    """Provides a superuser."""

    def create(**params):
        return User.objects.create_superuser(**params)

    return create


@pytest.fixture
def api_client_user(create_user):
    """Provides an authenticated api client."""
    user = create_user()
    client = APIClient()
    client.force_authenticate(user=user)

    return client


@pytest.fixture()
def avatar_file():
    content = (
        b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04"
        b"\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02"
        b"\x02\x4c\x01\x00\x3b"
    )
    avatar_file = SimpleUploadedFile("avatar.gif", content, content_type="image/gif")
    yield avatar_file

    os.remove(os.path.join(settings.MEDIA_ROOT, "avatars", avatar_file.name))
