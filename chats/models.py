from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()


class ChatRoom(models.Model):
    project = models.ForeignKey(
        "projects.Project", on_delete=models.CASCADE, related_name="chat_rooms"
    )
    visitor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="visited_chat_rooms"
    )
    slug = models.SlugField(unique=True, max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.project.id}-{self.visitor.id}")
        super().save(*args, **kwargs)

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
