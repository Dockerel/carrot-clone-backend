from rest_framework.serializers import ModelSerializer
from .models import ChattingRoom, Message
from users.serializer import JustUsernameSerializer


class ChattingRoomSerializer(ModelSerializer):
    users = JustUsernameSerializer(
        read_only=True,
        many=True,
    )

    class Meta:
        model = ChattingRoom
        fields = "__all__"


class TinyChattingRoomSerializer(ModelSerializer):
    class Meta:
        model = ChattingRoom
        fields = "__str__"


class MessageSerializer(ModelSerializer):
    user = JustUsernameSerializer(
        read_only=True,
    )

    class Meta:
        model = Message
        fields = (
            "text",
            "user",
            "created_at",
        )
