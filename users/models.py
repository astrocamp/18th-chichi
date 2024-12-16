from django.db import models


class User(models.Model):
    name = models.CharField(max_length=50)
    birthday = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=50)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.name
