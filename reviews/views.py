from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Review
from .serializer import ReviewSerializer
from users.models import User
from products.models import Product
from rest_framework.exceptions import NotFound


class Reviews(APIView):
    def get_object(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound

    def get(self, request, username):
        user = self.get_object(username)
        products = Product.objects.filter(
            owner=user,
            is_sold=True,
        )
        reviews = Review.objects.filter(product__in=products)
        serializer = ReviewSerializer(
            reviews,
            many=True,
        )
        return Response(serializer.data)
