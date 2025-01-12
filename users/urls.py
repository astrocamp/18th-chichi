from django.urls import path
from . import views

app_name = "profile"

urlpatterns = [
    path("new/", views.new, name="new"),
    path("edit/", views.edit, name="edit"),
]