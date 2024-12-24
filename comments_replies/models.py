from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class CommentsReplies(models.Model):
    content = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(null=True)
    account = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments_replies"
    )
