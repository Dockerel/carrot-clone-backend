from django.urls import path
from . import views

urlpatterns = [
    path("", views.Products.as_view()),
    path("@<str:username>", views.UserProduct.as_view()),
    path("<int:pk>", views.ProductDetail.as_view()),
    path("<int:pk>/sold", views.ProductSold.as_view()),
    path("<int:pk>/photos", views.ProductPhotoUpload.as_view()),
    path("<int:pk>/<str:username>", views.BuyProduct.as_view()),
]
