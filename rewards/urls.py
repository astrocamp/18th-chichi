from django.urls import path
from . import views

app_name = "rewards"

urlpatterns = [
    path("<int:id>", views.show, name="show"),
    path("<int:id>/edit", views.edit, name="edit"),
    path("<slug:slug>/content/", views.rewards_content, name="rewards_content"),
]
