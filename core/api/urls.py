from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from core.api import views

urlpatterns = [
    path("register/", views.UserRegisterAPIView.as_view(), name="register"),
    path("token/", TokenObtainPairView.as_view(), name="token"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("me/", views.UserMeApiView.as_view(), name="me"),
    path("me/password/", views.ChangePasswordApiView.as_view(), name="password"),
    path("me/avatar/", views.ChangeAvatarApiView.as_view(), name="avatar"),
]
