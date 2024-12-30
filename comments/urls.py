from django.urls import path
from .views import index, new, show, delete


app_name = "comments"

urlpatterns = [
    path("<slug:slug>/", show, name="show"),
    path("<slug:slug>/edit", edit, name="edit"),
    path("<slug:slug>/delete", delete, name="delete"),
    path("<int:id>/", show, name="show"),
    path("<int:id>/delete", delete, name="delete"),
]
