from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    """User Model Definition"""

    avatar = models.URLField(
        blank=True,
    )
    phone_nb = models.CharField(
        max_length=13,
    )
    address = models.CharField(
        max_length=250,
        blank=True,
        null=True,
    )
