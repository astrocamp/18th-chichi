from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepages.urls")),
    path("accounts/", include("accounts.urls")),
<<<<<<< HEAD
    path("projects/", include("projects.urls")),
    path("faqs/", include("faqs.urls")),
=======
    path("users/", include("users.urls")),
>>>>>>> 1b3fc01 (feat: issue/5 Users CRUD)
]

