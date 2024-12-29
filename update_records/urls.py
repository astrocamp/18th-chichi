from django.urls import path
from .views import index, new, show, edit, delete


app_name = "update_records"

urlpatterns = [
    path("<slug:slug>", show, name="show"),
    path("<slug:slug>/edit", edit, name="edit"),
    path("<slug:slug>/delete", delete, name="delete"),
]
