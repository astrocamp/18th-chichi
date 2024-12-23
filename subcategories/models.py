from django.db import models
<<<<<<< HEAD


class SubCategory(models.Model):
    title = models.CharField(max_length=20, unique=True)
=======
from categories.models import Category


class SubCategory(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="subcategories"
    )
>>>>>>> 0e4551c (feat: categories and subcategories relationship completed)

    def __str__(self):
        return self.title
