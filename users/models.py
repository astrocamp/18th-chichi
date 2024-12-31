from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    name = models.CharField(max_length=50)
    birthday = models.DateField(null=True, blank=True, default="")
    location = models.CharField(max_length=100, null=True, blank=True, default="")
    website = models.URLField(null=True, blank=True, default="")
    bio = models.TextField(null=True, blank=True, default="")
    phone = models.CharField(max_length=50, null=True, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)
    account = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to="profile_pictures/", null=True, blank=True
    )

    def __str__(self):
        return self.name
