from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone = models.CharField(max_length=9, null=True, blank=True)
    notification_push = models.BooleanField(default=False)
    notification_email = models.BooleanField(default=False)
    notification_favourites = models.BooleanField(default=False)

    def __str__(self):
        return self.username
