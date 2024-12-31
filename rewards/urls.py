from django.urls import path
from . import views

app_name = "rewards"

urlpatterns = [
    path("<int:id>", views.show, name="show"),
    path("<int:id>/edit", views.edit, name="edit"),
    path("<int:id>/delete", views.delete, name="delete"),
]
