from django.db import models
from common.models import CommonModel


class Photo(CommonModel):

    file = models.URLField()
    description = models.CharField(
        max_length=140,
    )
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="photos",
    )

    def __str__(self) -> str:
        return "Photo File"
