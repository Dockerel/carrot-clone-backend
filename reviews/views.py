from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Review
from .serializer import ReviewSerializer
from users.models import User
from products.models import Product
from products.models import Product
from rest_framework.exceptions import NotFound, NotAuthenticated


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


class MakeReview(APIView):
    def get_object(self, productPk):
        try:
            return Product.objects.get(pk=productPk)
        except Product.DoesNotExist:
            raise NotFound

    def post(self, request, productPk):
        product = self.get_object(productPk)
        user = request.user
        if user.username == product.buyer.username:
            serializer = ReviewSerializer(data=request.data)
            if serializer.is_valid():
                new_review = serializer.save(
                    user=user,
                    product=product,
                )
                serializer = ReviewSerializer(new_review)
                return Response(serializer.data)
            else:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            raise NotAuthenticated
