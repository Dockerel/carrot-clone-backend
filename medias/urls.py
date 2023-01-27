from django.urls import path
from . import views

urlpatterns = [
    path("get-url", views.GetUploadURL.as_view()),
    path("<int:pk>", views.PhotoDetail.as_view()),
]
