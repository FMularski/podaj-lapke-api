"""
    Tests of the core app's models.
"""
import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

User = get_user_model()


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


@pytest.mark.django_db
@pytest.mark.parametrize(
    "params",
    [
        {
            "username": "user",
            "email": "user@example.com",
            "password": "Test123",
            "phone": "123456789",
            "notification_push": True,
            "notification_email": True,
            "notification_favourites": True,
        },
        {
            "username": "user",
            "email": "user@example.com",
            "password": "Test123",
            "notification_push": True,
            "notification_email": False,
            "notification_favourites": True,
        },
        {
            "username": "user",
            "email": "user@example.com",
            "password": "Test123",
            "phone": "123456789",
        },
        {"username": "user", "email": "user@example.com", "password": "Test123"},
    ],
)
def test_create_user(create_user, params):
    """
    Test creating a regular user.
    """
    user = create_user(**params)

    assert User.objects.count() == 1
    assert check_password(params.pop("password"), user.password)

    for k, v in params.items():
        assert getattr(user, k) == v

    assert not user.is_staff
    assert not user.is_superuser


@pytest.mark.django_db
@pytest.mark.parametrize(
    "params",
    [
        {
            "username": "user",
            "email": "user@example.com",
            "password": "Test123",
            "phone": "123456789",
            "notification_push": True,
            "notification_email": True,
            "notification_favourites": True,
        },
        {
            "username": "user",
            "email": "user@example.com",
            "password": "Test123",
            "notification_push": True,
            "notification_email": False,
            "notification_favourites": True,
        },
        {
            "username": "user",
            "email": "user@example.com",
            "password": "Test123",
            "phone": "123456789",
        },
        {"username": "user", "email": "user@example.com", "password": "Test123"},
    ],
)
def test_create_superuser(create_superuser, params):
    """
    Test creating a regular user.
    """
    user = create_superuser(**params)

    assert User.objects.count() == 1
    assert check_password(params.pop("password"), user.password)

    for k, v in params.items():
        assert getattr(user, k) == v

    assert user.is_staff
    assert user.is_superuser
