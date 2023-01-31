from rest_framework.serializers import ModelSerializer
from users.serializer import TinyUserSerializer
from .models import Notification


class NotificationSerializer(ModelSerializer):

    receiver = TinyUserSerializer(
        read_only=True,
    )
    sender = TinyUserSerializer(
        read_only=True,
    )

    class Meta:
        model = Notification
        fields = (
            "pk",
            "receiver",
            "sender",
            "updated_at",
        )
