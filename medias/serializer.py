from rest_framework.serializers import ModelSerializer
from .models import Photo


class TinyPhotoSerializer(ModelSerializer):
    class Meta:
        model = Photo
        fields = ("file",)


class PhotoUploadSerializer(ModelSerializer):
    class Meta:
        model = Photo
        fields = (
            "description",
            "file",
        )


class PhotoDetailSerializer(ModelSerializer):
    class Meta:
        model = Photo
        fields = "__all__"
