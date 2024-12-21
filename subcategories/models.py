from django.db import models


class SubCategory(models.Model):
    title = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.title
