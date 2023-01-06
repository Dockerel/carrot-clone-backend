from rest_framework.serializers import ModelSerializer
from .models import Photo


class PhotoDetailSerializer(ModelSerializer):
    class Meta:
        model = Photo
        fields = "__all__"
