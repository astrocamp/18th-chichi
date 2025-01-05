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
            ("view_custom_category", "Can view custom category"),
            ("add_custom_category", "Can add custom category"),
            ("change_custom_category", "Can change custom category"),
            ("delete_custom_category", "Can delete custom category"),
        ]
