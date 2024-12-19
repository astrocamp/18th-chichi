from django.db import models

# Create your models here.
class CommentsReplies(models.Model):
    content = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(null=True)