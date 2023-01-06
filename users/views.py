from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ParseError, NotFound
from django.contrib.auth import authenticate, login, logout
from .models import User
from .serializer import SignUpSerializer, UserSerializer, PublicUserSerializer
from reviews.serializer import ReviewSerializer


class SignUp(APIView):
    def post(self, request):
        password = request.data.get("password")
        password_check = request.data.get("password_check")
        email = request.data.get("email")
        if User.objects.filter(email=email).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if password != password_check or not password or not password_check:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            new_user = serializer.save()
            new_user.set_password(password)
            new_user.save()
            serializer = SignUpSerializer(new_user)
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class Me(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


class SignIn(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError
        if not User.objects.filter(username=username).exists():
            return Response(
                {"error": "No username"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            login(request, user)
            return Response(
                {"ok": "Welcome"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "Wrong password"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class SignOut(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"ok": "Bye Bye"})


class PublicUser(APIView):
    def get_object(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound

    def get(self, request, username):
        user = self.get_object(username)
        serializer = PublicUserSerializer(user)
        return Response(serializer.data)


class PublicReview(APIView):
    def get_object(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound

    def get(self, request, username):
        user = self.get_object(username)
        reviews = user.reviews.all()
        serializer = ReviewSerializer(
            reviews,
            many=True,
        )
        return Response(serializer.data)

    # def post(self, request, username):
    #     user=self.get_object(username)
    #     serializer=ReviewSerializer(data=request.data)
    #     if serializer.is_valid():
    #         new_review=serializer.save()
