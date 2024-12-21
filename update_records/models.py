from django.db import models
from projects.models import Project

class UpdateRecord(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(null=True)
    project=models.ForeignKey(Project,on_delete=models.CASCADE,related_name="update_records")