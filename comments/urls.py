from django.urls import path
from .views import index, new, show, edit, delete

from comments_replies.views import (
    index as comments_replies_index,
    new as comments_replies_new,
)

app_name = "comments"

urlpatterns = [
    path("<slug:slug>/", show, name="show"),
    path("<slug:slug>/edit", edit, name="edit"),
    path("<slug:slug>/delete", delete, name="delete"),
    path(
        "<slug:slug>/comments_replies",
        comments_replies_index,
        name="comments_replies_index",
    ),
    path(
        "<slug:slug>/comments_replies/new",
        comments_replies_new,
        name="comments_replies_new",
    ),
]
