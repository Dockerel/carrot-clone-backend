from django.db import models
from django.contrib.auth.models import AbstractUser
from reviews.models import Review


class User(AbstractUser):

    """User Model Definition"""

    avatar = models.URLField(
        blank=True,
        null=True,
    )
    phone_nb = models.CharField(
        max_length=13,
        default="",
        blank=True,
        null=True,
    )
    address = models.CharField(
        max_length=250,
        default="",
    )
    detailed_address = models.CharField(
        max_length=250,
        default="",
    )

    def rating(user):
        products = user.products.all()
        reviews = Review.objects.filter(product__in=products)
        count = len(reviews)
        if count == 0:
            return 0
        else:
            total_rating = 0
            for review in reviews.values("rating"):
                total_rating += review["rating"]
            return round(total_rating / count, 2)
