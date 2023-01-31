from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from .models import Notification
from .serializer import NotificationSerializer
from users.models import User


class GetNotifications(APIView):
    def get(self, request):
        user = request.user
        notifications = Notification.objects.filter(
            Q(sender=user) | Q(receiver=user),
        )
        serializer = NotificationSerializer(
            notifications,
            many=True,
        )
        return Response(serializer.data)


class SendNotifications(APIView):
    def get_object(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound

    def post(self, request, username):

        user = self.get_object(username)
        userList = [user.username, request.user.username]
        userList.sort()

        if Notification.objects.filter(
            receiver=self.get_object(userList[0]),
            sender=self.get_object(
                userList[1],
            ),
        ).exists():
            return Response({"exists": "already exists"}, status=status.HTTP_400_BAD_REQUEST)
        if request.user.username != username:

            serializer = NotificationSerializer(data={})
            if serializer.is_valid():
                new_notification = serializer.save(
                    receiver=self.get_object(userList[0]),
                    sender=self.get_object(userList[1]),
                )
                serializer = NotificationSerializer(new_notification)
                return Response(serializer.data)
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
        )


class DeleteNotification(APIView):
    def delete(self, request, pk):
        ntfn = Notification.objects.get(pk=pk)
        ntfn.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
