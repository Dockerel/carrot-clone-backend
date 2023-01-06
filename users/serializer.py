from rest_framework.serializers import ModelSerializer
from .models import User


class TinyUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "pk",
            "username",
            "phone_nb",
        )


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "password",
            "last_login",
            "is_superuser",
            "is_staff",
            "is_active",
            "date_joined",
            "groups",
            "user_permissions",
        )


class PublicUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "avatar",
        )


class SignUpSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "phone_nb",
        )
