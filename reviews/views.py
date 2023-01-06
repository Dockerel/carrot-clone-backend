from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.response import Response
from products.models import Product
from .serializer import ReviewSerializer


class MakeReview(APIView):
    def get_object(self, name):
        try:
            return Product.objects.get(name=name)
        except Product.DoesNotExist:
            raise NotFound

    def post(self, request, product_name):
        product = self.get_object(product_name)
        buyer = product.buyer
        if buyer == request.user:
            serializer = ReviewSerializer(
                data=request.data,
            )
            if serializer.is_valid():
                new_review = serializer.save(
                    product=product,
                    user=buyer,
                )
                serializer = ReviewSerializer(new_review)
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            raise ParseError
