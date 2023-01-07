from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import status
from .models import ChattingRoom
from .serializer import ChattingRoomSerializer
from users.models import User


class ChattingRooms(APIView):
    def get(self, request):
        chattingRooms = ChattingRoom.objects.all()
        serializer = ChattingRoomSerializer(
            chattingRooms,
            many=True,
        )
        return Response(serializer.data)


class CreateChattingRoom(APIView):
    def get_user(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound

    def post(self, request, username):
        user = self.get_user(username)
        exists = ChattingRoom.objects.filter(users__in=[user, request.user]).exists()
        if exists:
            return Response(
                {"ok": "Chatting room already exists"},
                status=status.HTTP_200_OK,
            )
        serializer = ChattingRoomSerializer(data=request.data)
        if serializer.is_valid():
            new_chattingroom = serializer.save(
                user=[user, request.user],
            )
            serializer = ChattingRoomSerializer(new_chattingroom)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
