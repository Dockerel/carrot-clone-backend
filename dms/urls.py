from django.urls import path
from . import views

urlpatterns = [
    path("chatting-rooms/me", views.ChattingRooms.as_view()),
    path("chatting-rooms/@<str:username>/create", views.CreateChattingRoom.as_view()),
    path("chatting-rooms/<int:pk>/messages", views.Messages.as_view()),
    path("chatting-rooms/<int:pk>/update", views.UpdateChattingRoom.as_view()),
]
