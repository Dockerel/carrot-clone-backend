from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Product
from users.serializer import TinyUserSerializer
from medias.serializer import PhotoDetailSerializer, TinyPhotoSerializer


class ProductSerializer(ModelSerializer):

    is_owner = SerializerMethodField()
    buyer = TinyUserSerializer(
        read_only=True,
    )
    owner = TinyUserSerializer(
        read_only=True,
    )
    photos = TinyPhotoSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Product
        exclude = (
            "created_at",
            "updated_at",
        )

    def get_is_owner(self, product):
        request = self.context.get("request")
        if request:
            return product.owner == request.user
        return False


class ProductDetailSerializer(ModelSerializer):

    is_owner = SerializerMethodField()
    buyer = TinyUserSerializer(
        read_only=True,
    )
    owner = TinyUserSerializer(
        read_only=True,
    )
    photos = PhotoDetailSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Product
        exclude = ("updated_at",)

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


class ProductUserSerializer(ModelSerializer):
    photos = TinyPhotoSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Product
        fields = (
            "name",
            "price",
            "photos",
        )
