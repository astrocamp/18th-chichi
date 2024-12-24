from django.urls import path
from .views import index, new, show, edit, delete

from comments_replies.views import (
    index as comments_replies_index,
    new as comments_replies_new,
)

app_name = "comments"

urlpatterns = [
    path("<int:id>/", show, name="show"),
    path("<int:id>/edit", edit, name="edit"),
    path("<int:id>/delete", delete, name="delete"),
    path(
        "<int:id>/comments_replies",
        comments_replies_index,
        name="comments_replies_index",
    ),
    path(
        "<int:id>/comments_replies/new",
        comments_replies_new,
        name="comments_replies_new",
    ),
]
