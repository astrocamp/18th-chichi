from django.db import models
import datetime
from autoslug import AutoSlugField
import random
import string


def generate_random_slug():
    # 生成 8 位隨機字母數字組合
    letters_and_digits = string.ascii_lowercase + string.digits
    return "".join(random.choice(letters_and_digits) for i in range(8))

from projects.views import Project

def default_delivery_date():
    return datetime.date.today() + datetime.timedelta(days=7)

class Reward(models.Model):
    description = models.TextField(blank=True)
    title = models.CharField(max_length=300)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=0)
    ship_to = models.TextField()
    shipping_detail = models.TextField(blank=True)
    estimated_delivery = models.DateField(default=default_delivery_date)
    quantity = models.IntegerField(default=1)
    optional_adds_on = models.TextField(blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(null=True)
    project = models.ForeignKey(Project,on_delete=models.CASCADE)

    slug = AutoSlugField(
        populate_from=generate_random_slug,
        unique=True,
        editable=False,
        default=generate_random_slug,
        null=True,
        always_update=False,
    )
