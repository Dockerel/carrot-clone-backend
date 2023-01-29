from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from rest_framework import status
from rest_framework.exceptions import NotFound
from .models import Product
from .serializer import ProductSerializer, ProductDetailSerializer, ProductUserSerializer
from users.models import User
from medias.serializer import PhotoDetailSerializer


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
            product = serializer.save(
                owner=request.user,
            )
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
        serializer = ProductDetailSerializer(
            product,
            context={"request": request},
        )
        return Response(serializer.data)

    def put(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductDetailSerializer(
            product,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_product = serializer.save()
            serializer = ProductDetailSerializer(updated_product)
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


class BuyProduct(APIView):
    def get_product(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise NotFound

    def get_user(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound

    def put(self, request, pk, username):
        product = self.get_product(pk)
        owner = request.user
        if product.owner == owner:
            buyer = self.get_user(username)
            serializer = ProductSerializer(
                product,
                data=request.data,
                partial=True,
            )
            if serializer.is_valid() and product.buyer == None:
                updated_product = serializer.save(buyer=buyer)
                serializer = ProductSerializer(updated_product)
                return Response(serializer.data)
            else:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            raise NotAuthenticated


class ProductPhotoUpload(APIView):
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise NotFound

    def post(self, request, pk):
        product = self.get_object(pk)
        if not request.user.is_authenticated:
            raise NotAuthenticated
        if product.owner != request.user:
            raise PermissionDenied
        serializer = PhotoDetailSerializer(data=request.data)
        if serializer.is_valid():
            new_photo = serializer.save(product=product)
            serializer = PhotoDetailSerializer(new_photo)
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserProduct(APIView):
    def get_object(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound

    def get(self, request, username):
        user = self.get_object(username)
        products = Product.objects.filter(
            owner=user,
        )
        serializer = ProductUserSerializer(
            products,
            many=True,
        )
        return Response(serializer.data)


class ProductSold(APIView):
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise NotFound

    def post(self, request, pk):
        product = self.get_object(pk)
        data = {"is_sold": True}
        serializer = ProductSerializer(
            product,
            data=data,
            partial=True,
        )
        if serializer.is_valid():
            sold_product = serializer.save()
            serializer = ProductSerializer(sold_product)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class PurchaseHistory(APIView):
    def get(self, request, username):
        user = User.objects.get(username=username)
        products = Product.objects.filter(buyer=user)
        serializer = ProductSerializer(
            products,
            many=True,
        )
        return Response(serializer.data)


class ProductReviewUploaded(APIView):
    def put(self, request, pk):
        product = Product.objects.get(pk=pk)
        data = {"review_exists": True}
        serializer = ProductSerializer(
            product,
            data=data,
            partial=True,
        )
        if product.buyer.username == request.user.username:
            if serializer.is_valid():
                updated_product = serializer.save()
                serializer = ProductSerializer(updated_product)
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            raise NotAuthenticated
