from django.urls import path
from .views import index, subcategory_projects

app_name = "subcategories"

urlpatterns = [
    path("<int:category_id>/", index, name="index"),
    path(
        "<int:subcategory_id>/projects/",
        subcategory_projects,
        name="subcategory_projects",
    ),
]
