from django.db import models
from django.contrib.auth import get_user_model
from autoslug import AutoSlugField
import uuid

User = get_user_model()


def generate_random_slug(instance):
    return str(uuid.uuid4())[:8]


class ChatRoom(models.Model):
    project = models.ForeignKey(
        "projects.Project", on_delete=models.CASCADE, related_name="chat_rooms"
    )
    visitor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="visited_chat_rooms"
    )
    slug = AutoSlugField(
        populate_from=generate_random_slug, unique=True, max_length=100
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def participants(self):
        return [self.project.account, self.visitor]

    def __str__(self):
        return f"Chat {self.slug} - Project: {self.project.title}, Visitor: {self.visitor.username}"


class Message(models.Model):
    chat_room = models.ForeignKey(
        ChatRoom, on_delete=models.CASCADE, related_name="messages"
    )
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_messages"
    )
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}"
