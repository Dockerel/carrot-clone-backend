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

    def rating(user):
        count = user.reviews.count()
        if count == 0:
            return 0
        else:
            total_rating = 0
            for review in user.reviews.all().values("rating"):
                total_rating += review["rating"]
            return round(total_rating / count, 2)
