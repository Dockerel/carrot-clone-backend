from rest_framework.serializers import ModelSerializer
from .models import ChattingRoom, Message
from users.serializer import TinyUserSerializer


class ChattingRoomSerializer(ModelSerializer):
    users = TinyUserSerializer(
        read_only=True,
        many=True,
    )

    class Meta:
        model = ChattingRoom
        fields = "__all__"


class TinyChattingRoomSerializer(ModelSerializer):
    class Meta:
        model = ChattingRoom
        fields = ("__str__",)


class MessageSerializer(ModelSerializer):
    user = TinyUserSerializer(
        read_only=True,
    )

    room = TinyChattingRoomSerializer(
        read_only=True,
    )

    class Meta:
        model = Message
        fields = (
            "text",
            "user",
            "room",
        )
