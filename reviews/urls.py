from django.urls import path
from . import views

urlpatterns = [
    path("@<str:username>", views.Reviews.as_view()),
    path("<int:productPk>", views.MakeReview.as_view()),
]
