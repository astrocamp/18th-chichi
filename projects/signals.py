from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from projects.permissions import assign_view_project_permission


@receiver(post_save, sender=User)
def add_permission_to_new_user(sender, instance, created, **kwargs):
    if created:  # 僅在新使用者創建時執行
        assign_view_project_permission(instance)
