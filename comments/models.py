from django.db import models
from django.contrib.auth.models import User
from projects.models import Project
from autoslug import AutoSlugField
import random
import string


def generate_random_slug():
    # 生成 8 位隨機字母數字組合
    letters_and_digits = string.ascii_lowercase + string.digits
    return "".join(random.choice(letters_and_digits) for i in range(8))


class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="comments"
    )
    account = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    slug = AutoSlugField(
        populate_from=generate_random_slug,
        unique=True,
        editable=False,
        default=generate_random_slug,
        null=True,
        always_update=False,
    )

    parent = models.ForeignKey(
        "self", null=True, related_name="replies", on_delete=models.CASCADE
    )
