from django.db import models
from common.models import CommonModel


class Review(CommonModel):

    """Review from a User to a Room or Experience"""

    user = models.OneToOneField(
        "users.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="reviews",
    )
    product = models.OneToOneField(
        "products.Product",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    payload = models.TextField()
    rating = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"{self.user} / {self.rating}"
