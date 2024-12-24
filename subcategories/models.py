from django.db import models


class SubCategory(models.Model):
    title = models.CharField(max_length=20, unique=True)


from categories.models import Category


class SubCategory(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="subcategories"
    )

    def __str__(self):
        return self.title
