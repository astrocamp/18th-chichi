from django.db import models
from projects.models import Project
from autoslug import AutoSlugField
import random
import string


def generate_random_slug():
    # 生成 8 位隨機字母數字組合
    letters_and_digits = string.ascii_lowercase + string.digits
    return "".join(random.choice(letters_and_digits) for i in range(8))


class Faq(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    question = models.CharField(max_length=100)
    answer = models.TextField(null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(null=True)
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
            ("view_custom_faq", "Can view custom FAQ"),
            ("add_custom_faq", "Can add custom FAQ"),
            ("change_custom_faq", "Can change custom FAQ"),
            ("delete_custom_faq", "Can delete custom FAQ"),
        ]
