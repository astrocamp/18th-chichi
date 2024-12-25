from django.urls import path
from . import views

app_name = "rewards"

urlpatterns = [
    path("<slug:slug>", views.show, name="show"),
    path("<slug:slug>/edit", views.edit, name="edit"),
    path("<slug:slug>/delete", views.delete, name="delete"),
]
