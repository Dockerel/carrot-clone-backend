from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import status
from .models import ChattingRoom, Message
from .serializer import ChattingRoomSerializer, MessageSerializer
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


class Messages(APIView):
    def get_chattingroom(self, pk):
        try:
            return ChattingRoom.objects.get(pk=pk)
        except ChattingRoom.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        chattingRoom = self.get_chattingroom(pk)
        Messages = Message.objects.filter(room=chattingRoom)
        serializer = MessageSerializer(
            Messages,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, pk):
        chattingRoom = self.get_chattingroom(pk)
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            new_message = serializer.save(
                room=chattingRoom,
                user=request.user,
            )
            serializer = MessageSerializer(new_message)
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
