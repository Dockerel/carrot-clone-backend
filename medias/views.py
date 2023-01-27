import requests
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import status
from .models import Photo
from .serializer import PhotoDetailSerializer
from django.conf import settings


class PhotoDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Photo.objects.get(pk=pk)
        except Photo.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        photo = self.get_object(pk)
        serializer = PhotoDetailSerializer(photo)
        return Response(serializer.data)

    def delete(self, request, pk):
        photo = self.get_object(pk)
        if photo.product and photo.product.owner != request.user:
            raise PermissionDenied
        photo.delete()
        return Response(status=status.HTTP_200_OK)


class GetUploadURL(APIView):
    def post(self, request):
        url = f"https://api.cloudflare.com/client/v4/accounts/{settings.CF_ID}/images/v2/direct_upload"
        one_time_url = requests.post(url, headers={"Authorization": f"Bearer {settings.CF_TOKEN}"})
        response = one_time_url.json()
        if response.get("success"):
            result = response.get("result")
            print(result)
            return Response({"uploadURL": result.get("uploadURL")})
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
            )
