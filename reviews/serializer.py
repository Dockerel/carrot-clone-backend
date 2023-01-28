from rest_framework.serializers import ModelSerializer
from .models import Review
from products.serializer import TinyProductSerializer
from users.serializer import UserReviewSerializer


class ReviewSerializer(ModelSerializer):

    product = TinyProductSerializer(
        read_only=True,
    )
    user = UserReviewSerializer(
        read_only=True,
    )

    class Meta:
        model = Review
        fields = (
            "user",
            "product",
            "payload",
            "rating",
            "created_at",
        )
