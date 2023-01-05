from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import status
from rest_framework.exceptions import NotFound
from .models import Product
from .serializer import ProductSerializer


class Products(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_products = Product.objects.all()
        serializer = ProductSerializer(
            all_products,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class ProductDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(
            product,
            context={"request": request},
        )
        return Response(serializer.data)

    def put(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(
            product,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_product = serializer.save()
            serializer = ProductSerializer(updated_product)
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, pk):
        product = self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
