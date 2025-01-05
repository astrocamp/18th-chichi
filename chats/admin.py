from django.contrib import admin
from .models import ChatRoom, Message


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ["project", "visitor", "created_at", "updated_at"]
    list_filter = ["created_at", "updated_at"]
    search_fields = ["project__title", "visitor__username", "slug"]
    readonly_fields = ["slug"]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["chat_room", "sender", "content", "is_read", "created_at"]
    list_filter = ["is_read", "created_at"]
    search_fields = ["content", "sender__username"]
    readonly_fields = ["created_at"]
