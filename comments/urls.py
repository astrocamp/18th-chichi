from django.urls import path
from .views import index, new, show, delete


app_name = "comments"

urlpatterns = [
    path("<slug:slug>/", show, name="show"),
    path("<slug:slug>/delete", delete, name="delete"),
]
