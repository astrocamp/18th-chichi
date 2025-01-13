from django.db import models
from projects.models import Project
from autoslug import AutoSlugField
import random
import string
from django.contrib.auth.models import User


def generate_random_slug():
    # 生成 8 位隨機字母數字組合
    letters_and_digits = string.ascii_lowercase + string.digits
    return "".join(random.choice(letters_and_digits) for i in range(8))


class UpdateRecord(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True, db_index=True)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="update_records"
    )
    slug = AutoSlugField(
        populate_from=generate_random_slug,
        unique=True,
        editable=False,
        default=generate_random_slug,
        null=True,
        always_update=False,
    )

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="update_records")
