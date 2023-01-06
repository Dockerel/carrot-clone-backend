from rest_framework.serializers import ModelSerializer
from .models import Review
from products.serializer import TinyProductSerializer


class ReviewSerializer(ModelSerializer):

    product = TinyProductSerializer(
        read_only=True,
    )

    class Meta:
        model = Review
        fields = (
            "product",
            "payload",
            "rating",
        )
