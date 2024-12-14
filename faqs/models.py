from django.db import models

class Faq(models.Model):
    question = models.CharField(max_length=100)
    answer = models.TextField(null=True)
    create_at = models.DateTimeField(auto_now_add=True)  
    update_at = models.DateTimeField(null=True)  
