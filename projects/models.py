from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from autoslug import AutoSlugField
from django.db.models import Sum
from categories.models import Category
import random
import string
from django.utils import timezone


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
    cover_image = models.FileField(upload_to="cover_img/", null=True)
    raised_amount = models.DecimalField(null=True, decimal_places=0, max_digits=10)
    goal_amount = models.DecimalField(decimal_places=0, max_digits=10)
    start_at = models.DateTimeField(null=True)
    end_at = models.DateTimeField()
    story = models.TextField()
    categories = models.ManyToManyField(
        Category,
        through="ProjectCategory",
        through_fields=("project", "category", "subcategory"),
        related_name="projects",
    )
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

    def remaining_days(self):
        now = timezone.now()
        if now > self.end_at:
            return 0
        return (self.end_at - now).days

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

    def update_raised_amount(self):
        """
        更新已籌金額：從已付款的訂單中計算
        """
        from payments.models import Order
        from rewards.models import Reward

        # 計算來自回饋方案的訂單金額
        reward_orders_amount = (
            Order.objects.filter(reward__project=self, paid=True).aggregate(
                total=Sum("amount")
            )["total"]
            or 0
        )

        # 計算來自自由贊助的訂單金額（通過訂單描述判斷）
        free_orders_amount = (
            Order.objects.filter(
                description__startswith=f"{self.title} - 自由贊助", paid=True
            ).aggregate(total=Sum("amount"))["total"]
            or 0
        )

        # 更新總金額
        self.raised_amount = reward_orders_amount + free_orders_amount
        self.save()

    def get_backers_count(self):
        """
        獲取贊助人數：計算已付款的不重複贊助者數量
        """
        from .models import Sponsor

        return (
            Sponsor.objects.filter(project=self, status="paid")
            .values("account")
            .distinct()
            .count()
        )

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

    def __str__(self):
        return self.title


class CollectProject(models.Model):
    account = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)


class FavoritePrject(models.Model):
    account = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)


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


class ProjectCategory(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="project_categories"
    )
    subcategory = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="subcategory_project_categories",
    )
