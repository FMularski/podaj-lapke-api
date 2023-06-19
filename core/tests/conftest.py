"""
    Fixtures required for tests of the core app.
"""

import tempfile

import pytest
from django.contrib.auth import get_user_model
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
