from django.urls import path
from . import views

urlpatterns = [
    path("", views.SignUp.as_view()),
    path("me", views.Me.as_view()),
    path("signin", views.SignIn.as_view()),
    path("signout", views.SignOut.as_view()),
    path("@<str:username>", views.PublicUser.as_view()),
    path("@<str:username>/review", views.PublicReview.as_view()),
]
