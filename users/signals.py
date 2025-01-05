from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Permission
from .models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            name=instance.username,
            account=instance,
            location="",
            bio="",
            birthday=None,
            website="",
        )


@receiver(post_save, sender=User)
def assign_permissions(sender, instance, created, **kwargs):
    if created:
        permission = Permission.objects.get(codename="view_project")
        instance.user_permissions.add(permission)
