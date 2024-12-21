from django.urls import path
from .views import subindex

app_name = "subcategories"

urlpatterns = [
    path("", subindex, name="subindex"),
]
