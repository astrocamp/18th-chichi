from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepages.urls")),
    path("projects/", include("projects.urls")),
    path("faqs/", include("faqs.urls")),
    path("users/", include("users.urls")),
    path("accounts/", include("allauth.urls")),
<<<<<<< HEAD
=======
    path('comments/', include("comments.urls")),
>>>>>>> 205bf46 (feat:comments CRD completed)
]
