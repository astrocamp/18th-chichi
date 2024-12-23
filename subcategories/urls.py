from django.urls import path
<<<<<<< HEAD
from .views import subindex
=======
from .views import index
>>>>>>> 0e4551c (feat: categories and subcategories relationship completed)

app_name = "subcategories"

urlpatterns = [
<<<<<<< HEAD
    path("", subindex, name="subindex"),
=======
    path("<int:category_id>/", index, name="index"),
>>>>>>> 0e4551c (feat: categories and subcategories relationship completed)
]
