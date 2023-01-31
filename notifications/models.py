from django.db import models
from common.models import CommonModel


class Notification(CommonModel):

    """Notification Model Definition"""

    receiver = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="+",
    )
    sender = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="+",
    )
