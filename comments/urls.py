from django.urls import path
from .views import new, reply, delete, reply_form


app_name = "comments"

urlpatterns = [
    path("<slug:slug>/new/", new, name="new"),
    path("<slug:slug>/reply/<slug:comment_slug>/", reply, name="reply"),
    path("<slug:slug>/delete/<slug:comment_slug>/", delete, name="delete"),
    path("<slug:slug>/reply_form/<slug:comment_slug>/", reply_form, name="reply_form"),
]
