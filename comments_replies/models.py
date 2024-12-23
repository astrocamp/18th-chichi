from django.db import models
from comments.models import Comment


# Create your models here.
class CommentsReplies(models.Model):
    content = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
