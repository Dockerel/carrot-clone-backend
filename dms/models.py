from django.db import models
from common.models import CommonModel


class ChattingRoom(CommonModel):

    """Room Model Definition"""

    users = models.ManyToManyField(
        "users.User",
        related_name="chatting_rooms",
    )

    def __str__(self) -> str:
        return f"Chatting Room : {self.pk}"


class Message(CommonModel):

    """Message Model Definition"""

    text = models.TextField()
    user = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    room = models.ForeignKey(
        "dms.ChattingRoom",
        on_delete=models.CASCADE,
        related_name="messages",
    )

    def __str__(self) -> str:
        return f"{self.user} says: {self.text}"
