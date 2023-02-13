from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, NotAuthenticated
from rest_framework import status
from .models import ChattingRoom, Message
from .serializer import ChattingRoomSerializer, MessageSerializer
from users.models import User


class ChattingRooms(APIView):
    def get(self, request):
        user = request.user
        chattingRooms = user.chatting_rooms.all()
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
        user1 = self.get_user(username)
        user2 = request.user
        room1 = ChattingRoom.objects.filter(users__in=[user1])
        room2 = ChattingRoom.objects.filter(users__in=[user2])
        room = room1.intersection(room2)
        if room:
            serializer = ChattingRoomSerializer(room)
            return Response(
                {"No": "Chatting room already exists"},
                status=status.HTTP_302_FOUND,
            )
        else:
            serializer = ChattingRoomSerializer(
                data=request.data,
            )
            if serializer.is_valid():
                new_chattingroom = serializer.save(
                    users=[user1, user2],
                )
                serializer = ChattingRoomSerializer(
                    new_chattingroom,
                )
                return Response(serializer.data)
            else:
                return Response(serializer.errors)


class Messages(APIView):
    def get_chattingroom(self, pk):
        try:
            return ChattingRoom.objects.get(pk=pk)
        except ChattingRoom.DoesNotExist:
            raise NotFound

    def authenticate_dms(self, user, chattingroom):
        if user not in chattingroom:
            return False
        return True

    def get(self, request, pk):
        chattingRoom = self.get_chattingroom(pk)
        if not self.authenticate_dms(request.user, chattingRoom.users.all()):
            raise NotAuthenticated
        messages = Message.objects.filter(room=chattingRoom)
        serializer = MessageSerializer(
            messages,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, pk):
        chattingRoom = self.get_chattingroom(pk)
        if not self.authenticate_dms(request.user, chattingRoom.users.all()):
            raise NotAuthenticated
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
