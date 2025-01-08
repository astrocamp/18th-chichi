from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=100, unique=True)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )

    def __str__(self):
        return self.title

    class Meta:
        permissions = [
            ("view_category", "Can view category"),
            ("add_category", "Can add category"),
            ("change_category", "Can change category"),
            ("delete_category", "Can delete category"),
        ]
