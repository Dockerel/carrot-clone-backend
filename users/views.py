import requests
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ParseError, NotFound
from django.contrib.auth import authenticate, login, logout
from .models import User
from .serializer import SignUpSerializer, UserSerializer, PublicUserSerializer
from reviews.serializer import ReviewSerializer
from django.conf import settings


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

    def put(self, request):
        user = request.user
        serializer = UserSerializer(
            user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_user = serializer.save()
            serializer = UserSerializer(updated_user)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                serializer.errors,
                status=status._400,
            )

    def delete(self, request):
        user = request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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


class githubLogin(APIView):
    def post(self, request):
        try:
            code = request.data.get("code")
            client_id = "d877e128569aba7998cb"
            access_token = requests.post(
                f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={settings.GH_SECRET}&code={code}",
                headers={"Accept": "application/json"},
            )
            access_token = access_token.json().get("access_token")
            user_data = requests.get(
                "https://api.github.com/user",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json",
                },
            )
            user_data = user_data.json()
            user_emails = requests.get(
                "https://api.github.com/user/emails",
                headers={"Authorization": f"Bearer {access_token}", "Accept": "application/json"},
            )
            user_emails = user_emails.json()
            try:
                user = User.objects.get(email=user_emails[0]["email"])
                login(request, user)
                return Response(status=status.HTTP_200_OK)
            except User.DoesNotExist:
                user = User.objects.create(
                    username=user_data.get("login"),
                    email=user_emails[0]["email"],
                    avatar=user_data.get("avatar_url"),
                )
                user.set_unusable_password()
                user.save()
                login(request, user)
            return Response(status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class kakaoLogin(APIView):
    def post(self, request):
        try:
            code = request.data.get("code")
            client_id = "792bcd646d46d44b3f56dd4039e63fc7"
            redirect_url = "http://127.0.0.1:3000/social/kakao"
            access_token = requests.post(
                f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_url}&code={code}",
                headers={
                    "Accept": "application/json",
                    "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
                },
            )
            access_token = access_token.json().get("access_token")
            user_data = requests.get(
                "https://kapi.kakao.com/v2/user/me",
                headers={
                    "Accept": "application/json",
                    "Authorization": f"Bearer {access_token}",
                    "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
                },
            )
            user_email = user_data.json().get("kakao_account").get("email")
            user_data = user_data.json().get("kakao_account").get("profile")
            try:
                user = User.objects.get(email=user_email)
                login(request, user)
                return Response(status=status.HTTP_200_OK)
            except User.DoesNotExist:
                user = User.objects.create(
                    username=user_data.get("nickname"),
                    email=user_email,
                    avatar=user_data.get("profile_image_url"),
                )
                user.set_unusable_password()
                user.save()
                login(request, user)
            return Response(status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class naverLogin(APIView):
    def post(self, request):
        try:
            code = request.data.get("code")
            state = request.data.get("state")
            access_token = requests.post(
                f"https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id=pJIeDRqJex8LshmCWf0R&client_secret={settings.NAVER_SECRET}&code={code}&state={state}",
                headers={
                    "Accept": "application/json",
                },
            )
            access_token = access_token.json().get("access_token")
            user_data = requests.post(
                "https://openapi.naver.com/v1/nid/me",
                headers={
                    "Accept": "application/json",
                    "Authorization": f"Bearer {access_token}",
                },
            )
            user_data = user_data.json().get("response")
            try:
                user = User.objects.get(email=user_data.get("email"))
                login(request, user)
                return Response(status=status.HTTP_200_OK)
            except User.DoesNotExist:
                user = User.objects.create(
                    username=user_data.get("name"),
                    email=user_data.get("email"),
                    avatar=user_data.get("profile_image"),
                )
                user.set_unusable_password()
                user.save()
                login(request, user)
            return Response(status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
