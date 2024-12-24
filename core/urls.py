from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepages.urls")),
    path("projects/", include("projects.urls")),
    path("faqs/", include("faqs.urls")),
    path("profiles/", include("users.urls")),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("allauth.urls")),
    path("comments/", include("comments.urls")),
    path("categories/", include("categories.urls")),
    path("rewards/", include("rewards.urls")),
    path("subcategories/", include("subcategories.urls")),
    path("comments_replies/",include("comments_replies.urls")),
    path('update_records/', include("update_records.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
