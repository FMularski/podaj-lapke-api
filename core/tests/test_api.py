"""
    Test api endpoints for the core app.
"""
import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.shortcuts import reverse
from rest_framework import status

from core.api import serializers

User = get_user_model()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "body", ({"username": "user", "email": "user@example.com", "password": "pass123"},)
)
def test_register_user_201(api_client, body):
    """Test a successful registration."""
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
    """Test an unsuccessful registration."""
    url = reverse("register")
    res = api_client.post(url, data=body)

    assert res.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
@pytest.mark.parametrize(
    "body",
    [
        {"username": "user", "email": "user@example.com", "password": "pass123"},
    ],
)
def test_login_200(create_user, api_client, body):
    """Test a successful login."""
    create_user(**body)
    body.pop("email")

    url = reverse("token")
    res = api_client.post(url, data=body)

    assert res.status_code == status.HTTP_200_OK
    assert "access" in res.data.keys()
    assert "refresh" in res.data.keys()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "body",
    [
        {"username": "user"},
        {"password": "pass123"},
        {},
    ],
)
def test_login_400(api_client, body):
    """Test unsuccessful login - insufficient data."""
    url = reverse("token")
    res = api_client.post(url, data=body)

    assert res.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
@pytest.mark.parametrize(
    "body",
    [
        {"username": "user", "password": "pass123"},
    ],
)
def test_login_401(api_client, body):
    """Test unsuccessful login - invalid credentials."""
    url = reverse("token")
    res = api_client.post(url, data=body)

    assert res.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_refresh_200(api_client, create_user):
    """Test a successful token refresh."""
    user = create_user(username="user", email="user@example.com", password="pass123")

    token_url = reverse("token")
    refresh_token = api_client.post(
        token_url, {"username": user.username, "password": "pass123"}
    ).data["refresh"]

    refresh_url = reverse("refresh")

    res = api_client.post(refresh_url, data={"refresh": refresh_token})

    assert res.status_code == status.HTTP_200_OK
    assert "access" in res.data.keys()


@pytest.mark.django_db
def test_refresh_401(api_client):
    """Test an unseccessful token refresh - invalid token."""
    refresh_url = reverse("refresh")

    res = api_client.post(refresh_url, data={"refresh": "invalid token"})

    assert res.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_get_user_details_401(api_client):
    """Test calling GET /me/ without token returns 401."""
    url = reverse("me")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_get_user_details_200(create_user, api_client):
    """Test calling GET /me/ returns details of authenticated user."""
    user = create_user()
    api_client.force_authenticate(user)
    url = reverse("me")
    response = api_client.get(url)

    serializer = serializers.UserSerializer(user)

    assert response.status_code == status.HTTP_200_OK

    for key in response.data:
        if not key == "avatar":
            assert response.data[key] == serializer.data[key]
        else:
            assert response.data[key] == "http://testserver" + serializer.data[key]


@pytest.mark.django_db
def test_update_user_details_401(api_client):
    """Test calling PATCH /me/ without token returns 401."""
    url = reverse("me")
    response = api_client.patch(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
@pytest.mark.parametrize(
    "body, xstatus",
    (
        (
            {
                "first_name": "new",
                "last_name": "new",
                "email": "new@example.com",
                "phone": "234567891",
            },
            status.HTTP_200_OK,
        ),
        (
            {"first_name": "new", "last_name": "new", "email": "new@example.com"},
            status.HTTP_200_OK,
        ),
        ({"first_name": "new", "last_name": "new"}, status.HTTP_200_OK),
        ({"first_name": "new"}, status.HTTP_200_OK),
        ({"email": "invalid"}, status.HTTP_400_BAD_REQUEST),
        ({"email": ""}, status.HTTP_400_BAD_REQUEST),
        ({"phone": "123"}, status.HTTP_400_BAD_REQUEST),
    ),
)
def test_update_user_details(api_client_user, body, xstatus):
    url = reverse("me")
    response = api_client_user.patch(url, data=body, format="json")

    assert response.status_code == xstatus
    if response.status_code == status.HTTP_200_OK:
        user = User.objects.get(pk=response.data["id"])
        for k, v in body.items():
            assert getattr(user, k) == v
