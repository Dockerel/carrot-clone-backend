from django.urls import path
from . import views

urlpatterns = [
    path("me", views.GetNotifications.as_view()),
    path("<str:username>", views.SendNotifications.as_view()),
    path("<int:pk>/delete", views.DeleteNotification.as_view()),
]
