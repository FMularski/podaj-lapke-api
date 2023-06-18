from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=9, null=True, blank=True)
    notification_push = models.BooleanField(default=False)
    notification_email = models.BooleanField(default=False)
    notification_favourites = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to="avatars", null=True, blank=True)

    def __str__(self):
        return self.username
