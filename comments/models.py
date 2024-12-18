from django.db import models
from django.contrib.auth.models import User
from projects.models import Project


class Comment(models.Model):
    content = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(null=True)
    project=models.ForeignKey(Project,on_delete=models.CASCADE,related_name="comments")

