from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/products/", include("products.urls")),
    path("api/v1/users/", include("users.urls")),
    path("api/v1/photos/", include("medias.urls")),
    path("api/v1/reviews/", include("reviews.urls")),
    path("api/v1/dms/", include("dms.urls")),
    path("api/v1/notifications/", include("notifications.urls")),
]
