from django.urls import path
from .views import index

app_name = "subcategories"

urlpatterns = [
    path("", index, name="index"),
    path("<int:category_id>/", index, name="index"),
]
