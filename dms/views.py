from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
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
    def get_object(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound

    def post(self, request, username):
        # 이미 user1 user2 가 있는 채팅방이 만들어져있으면 안만드는걸로....
        user = self.get_object(username)
        serializer = ChattingRoomSerializer(data=request.data)
        if serializer.is_valid():
            new_chattingroom = serializer.save(
                user=[user, request.user],
            )
            serializer = ChattingRoomSerializer(new_chattingroom)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
