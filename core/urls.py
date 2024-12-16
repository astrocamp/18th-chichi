from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
<<<<<<< HEAD
    path("", include("homepages.urls")),
    path("accounts/", include("accounts.urls")),
<<<<<<< HEAD
    path("projects/", include("projects.urls")),
    path("faqs/", include("faqs.urls")),
=======
=======
    path(
        "",
        include("homepages.urls"),
    ),
    path(
        "accounts/",
        include("accounts.urls"),
    ),
    path("projects/", include("projects.urls")),
>>>>>>> 91d25ef (fix:setting/url/)
    path("users/", include("users.urls")),
]
