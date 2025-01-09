from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from projects.models import Project


# 為使用者分配權限
def assign_view_project_permission(user):
    content_type = ContentType.objects.get_for_model(Project)
    permission = Permission.objects.get(
        codename="view_project", content_type=content_type
    )
    user.user_permissions.add(permission)
