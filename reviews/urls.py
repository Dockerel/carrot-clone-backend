from django.urls import path
from . import views

urlpatterns = [
    path("<str:product_name>", views.MakeReview.as_view()),
]
