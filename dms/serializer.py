from rest_framework.serializers import ModelSerializer
from .models import ChattingRoom
from users.serializer import TinyUserSerializer


class ChattingRoomSerializer(ModelSerializer):
    users = TinyUserSerializer(
        read_only=True,
        many=True,
    )

    class Meta:
        model = ChattingRoom
        fields = "__all__"
