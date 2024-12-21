from django.db import models
from projects.models import Project

class Faq(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    question = models.CharField(max_length=100)
    answer = models.TextField(null=True)
    create_at = models.DateTimeField(auto_now_add=True)  
    update_at = models.DateTimeField(null=True)  
