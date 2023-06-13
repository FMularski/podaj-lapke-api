"""
    Fixtures required for tests of the core app.
"""

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

    def create(**params):
        return User.objects.create_user(**params)

    return create


@pytest.fixture
def create_superuser():
    """Provides a superuser."""

    def create(**params):
        return User.objects.create_superuser(**params)

    return create
