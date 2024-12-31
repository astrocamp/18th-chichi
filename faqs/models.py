from django.db import models
from projects.models import Project

class Faq(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    question = models.CharField(max_length=100)
    answer = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  
    position = models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ["position"]
