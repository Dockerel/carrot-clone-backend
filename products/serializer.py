from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Product
from users.serializer import TinyUserSerializer


class ProductSerializer(ModelSerializer):

    is_owner = SerializerMethodField()
    buyer = TinyUserSerializer(
        read_only=True,
    )

    class Meta:
        model = Product
        exclude = (
            "owner",
            "created_at",
            "updated_at",
        )

    def get_is_owner(self, product):
        request = self.context.get("request")
        if request:
            return product.owner == request.user
        return False


class TinyProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "name",
            "price",
        )
