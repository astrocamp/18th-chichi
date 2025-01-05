from django.db import models
from projects.models import Project
from autoslug import AutoSlugField
import random
import string


def generate_random_slug():
    # 生成 8 位隨機字母數字組合
    letters_and_digits = string.ascii_lowercase + string.digits
    return "".join(random.choice(letters_and_digits) for i in range(8))


class UpdateRecord(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(null=True)
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

    class Meta:
        permissions = [
            ("view_custom_updaterecord", "Can view custom update record"),
            ("add_custom_updaterecord", "Can add custom update record"),
            ("change_custom_updaterecord", "Can change custom update record"),
            ("delete_custom_updaterecord", "Can delete custom update record"),
        ]
