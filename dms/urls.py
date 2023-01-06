from django.urls import path
from . import views

urlpatterns = [
    path("", views.ChattingRooms.as_view()),
    path("<str:username>", views.CreateChattingRoom.as_view()),
]
