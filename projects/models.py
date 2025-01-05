from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from autoslug import AutoSlugField
import random
import string


def generate_random_slug():
    # 生成 8 位隨機字母數字組合
    letters_and_digits = string.ascii_lowercase + string.digits
    return "".join(random.choice(letters_and_digits) for i in range(8))


class Project(models.Model):
    STATUS_CHOICES = [
        ("pending", "待上架"),
        ("live", "已上架"),
        ("ended", "已下架"),
    ]
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100, null=True)
    cover_image = models.FileField(upload_to="uploads/", null=True)
    raised_amount = models.DecimalField(null=True, decimal_places=0, max_digits=10)
    goal_amount = models.DecimalField(decimal_places=0, max_digits=10)
    start_at = models.DateTimeField(null=True)
    end_at = models.DateTimeField()
    story = models.TextField()
    location = models.CharField(null=True, max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    account = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="pending",
    )
    slug = AutoSlugField(
        populate_from=generate_random_slug,
        unique=True,
        editable=False,
        default=generate_random_slug,
        null=True,
        always_update=False,
    )
    collect_account = models.ManyToManyField(
        User,
        related_name="collect_projects",
        through="CollectProject",
        through_fields=("project", "account"),
    )

    def update_status(self):
        """
        更新專案狀態：根據時間設定自動上架或下架
        """
        current_time = now()
        if self.status == "pending" and self.start_at and current_time >= self.start_at:
            self.status = "live"
            self.save()
        elif self.status == "live" and self.end_at and current_time >= self.end_at:
            self.status = "ended"
            self.save()

    favorite_users = models.ManyToManyField(
        User,
        related_name="favorite_users",
        through="FavoritePrject",
        through_fields=("project", "account"),
    )

    sponsor_account = models.ManyToManyField(
        User,
        related_name="sponsor_project",
        through="Sponsor",
        through_fields=("project", "account"),
    )

    class Meta:
        permissions = [
            ("view_custom_project", "Can view custom project"),
            ("add_custom_project", "Can add custom project"),
            ("change_custom_project", "Can change custom project"),
            ("delete_custom_project", "Can delete custom project"),
        ]


class CollectProject(models.Model):
    account = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = [
            ("view_custom_collectproject", "Can view custom collect project"),
            ("add_custom_collectproject", "Can add custom collect project"),
            ("change_custom_collectproject", "Can change custom collect project"),
            ("delete_custom_collectproject", "Can delete custom collect project"),
        ]


class FavoritePrject(models.Model):
    account = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = [
            ("view_custom_favoriteproject", "Can view custom favorite project"),
            ("add_custom_favoriteproject", "Can add custom favorite project"),
            ("change_custom_favoriteproject", "Can change custom favorite project"),
            ("delete_custom_favoriteproject", "Can delete custom favorite project"),
        ]


class Sponsor(models.Model):
    from rewards.models import Reward

    account = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    reward = models.ForeignKey(Reward, on_delete=models.CASCADE, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=0)
    created_at = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("failed", "Failed"),
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="pending",
    )

    class Meta:
        permissions = [
            ("view_custom_sponsor", "Can view custom sponsor"),
            ("add_custom_sponsor", "Can add custom sponsor"),
            ("change_custom_sponsor", "Can change custom sponsor"),
            ("delete_custom_sponsor", "Can delete custom sponsor"),
        ]
