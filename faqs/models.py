from django.db import models

class Faq(models.Model):
    question = models.CharField(max_length=100)
    answer = models.TextField(null=True)