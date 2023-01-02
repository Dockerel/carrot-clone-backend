from django.db import models
from common.models import CommonModel


class Product(CommonModel):

    """Product Model Definition"""

    class productKindChoices(models.TextChoices):
        ELECTRONICS = ("electronics", "Electronics")
        FURNITURES = ("furnitures", "Furnitures")
        KITCHEN = ("kitchen", "Kitchen")
        CLOTHES = ("clothes", "Clothes")
        TICKETS = ("tickets", "Tickets")
        PLANTS = ("plants", "Plants")
        ETC = ("etc", "Etc")

    name = models.CharField(
        max_length=180,
    )
    price = models.IntegerField()
    description = models.TextField()
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="products",
    )
    kind = models.CharField(
        max_length=30,
        choices=productKindChoices.choices,
    )
    is_reported = models.BooleanField(
        default=False,
    )
    is_sold = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return self.name
