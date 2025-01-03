from django.urls import path
from .views import new, reply, delete, load_reply_form


app_name = "comments"

urlpatterns = [
    path("<slug:slug>/new/", new, name="new"),
    path("<slug:slug>/reply/<slug:comment_slug>/", reply, name="reply"),
    path("<slug:slug>/delete/<slug:comment_slug>/", delete, name="delete"),
    path(
        "<slug:slug>/form/<slug:comment_slug>/", load_reply_form, name="load_reply_form"
    ),
]
