from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepages.urls")),
    path("projects/", include("projects.urls")),
    path("faqs/", include("faqs.urls")),
    path("users/", include("users.urls")),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("allauth.urls")),
    path("comments/", include("comments.urls")),
    path("categories/", include("categories.urls")),
    path("rewards/", include("rewards.urls")),
    path("comments_replies/",include("comments_replies.urls")),
    path('update_records/', include("update_records.urls")),
]
