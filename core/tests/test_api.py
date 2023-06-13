"""
    Test api endpoints for the core app.
"""
import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.shortcuts import reverse
from rest_framework import status

User = get_user_model()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "body", ({"username": "user", "email": "user@example.com", "password": "pass123"},)
)
def test_register_user_201(api_client, body):
    url = reverse("register")
    res = api_client.post(url, data=body)

    assert res.status_code == status.HTTP_201_CREATED
    user = User.objects.get(pk=res.data["id"])

    assert user.username == body["username"]
    assert user.email == body["email"]
    assert check_password(body["password"], user.password)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "body",
    (
        {"username": "user", "email": "user@example.com"},
        {"username": "user", "password": "pass123"},
        {"email": "user@example.com", "password": "pass123"},
        {"password": "pass123"},
        {"username": "user"},
        {},
    ),
)
def test_register_user_400(api_client, body):
    url = reverse("register")
    res = api_client.post(url, data=body)

    assert res.status_code == status.HTTP_400_BAD_REQUEST
