from django.urls import path
from . import views

app_name = "chats"

urlpatterns = [
    path("", views.chat_list_all, name="list_all"),
    path("create/<slug:project_slug>/", views.create_chat, name="create"),
    path("<slug:project_slug>/", views.chat_list, name="list"),
    path("room/<slug:room_slug>/", views.chat_room, name="room"),
]
