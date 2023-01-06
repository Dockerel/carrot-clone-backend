from rest_framework.serializers import ModelSerializer
from .models import Review
from products.serializer import TinyProductSerializer
from users.serializer import TinyUserSerializer


class ReviewSerializer(ModelSerializer):

    product = TinyProductSerializer(
        read_only=True,
    )
    user = TinyUserSerializer(
        read_only=True,
    )

    class Meta:
        model = Review
        fields = (
            "user",
            "product",
            "payload",
            "rating",
        )
