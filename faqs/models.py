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
    slug = AutoSlugField(
        populate_from=generate_random_slug,
        unique=True,
        editable=False,
        default=generate_random_slug,
        null=True,
        always_update=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  
    position = models.PositiveIntegerField(default=0)
    deleted_at = models.DateTimeField(null=True, db_index=True)

    class Meta:
        ordering = ["position"]
