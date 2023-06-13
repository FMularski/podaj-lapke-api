"""
    Tests of the core app's models.
"""
import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.core.management import call_command

User = get_user_model()


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


@pytest.mark.django_db
def test_load_user_fixture():
    """Test loading user from a fixture."""
    call_command("loaddata", "user.json")
    assert User.objects.count() == 1
