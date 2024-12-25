from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepages.urls")),
    path("profile/", include("users.urls")),
    path("projects/", include("projects.urls")),
    path("faqs/", include("faqs.urls")),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("allauth.urls")),
    path("comments/", include("comments.urls")),
    path("categories/", include("categories.urls")),
    path("rewards/", include("rewards.urls")),
    path("update_records/", include("update_records.urls")),
    path('payments/', include("payments.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
