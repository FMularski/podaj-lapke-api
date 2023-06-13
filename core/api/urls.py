from django.urls import path

from core.api import views

urlpatterns = [
    path("register/", views.UserRegisterAPIView.as_view(), name="register"),
]
