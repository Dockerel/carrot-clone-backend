from django.db import models
from common.models import CommonModel


class ChattingRoom(CommonModel):

    """Room Model Definition"""

    sender = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="chatting_rooms_sender",
    )
    receiver = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="chatting_rooms_receiver",
    )

    def __str__(self) -> str:
        return f"Chatting Room : {self.sender} / {self.receiver}"


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
