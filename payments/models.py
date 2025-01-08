from django.db import models
from rewards.models import Reward
from django.contrib.auth.models import User
from decimal import Decimal


class Order(models.Model):
    order_id = models.CharField(max_length=100, unique=True)
    amount = models.IntegerField()
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    reward = models.ForeignKey(
        Reward, on_delete=models.CASCADE, related_name="orders", null=True, blank=True
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        if self.reward:
            return f"Order {self.order_id} - {self.reward.title}"
        return f"Order {self.order_id} - 自由贊助"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.paid:
            # 更新專案的 raised_amount
            project = self.reward.project if self.reward else None
            if not project and self.reward is None:
                # 如果是自由贊助，從 description 中取得專案標題
                from projects.models import Project

                project_title = self.description.split(" - ")[0]
                project = Project.objects.filter(title=project_title).first()

            if project:
                # 建立或更新 Sponsor 記錄
                from projects.models import Sponsor

                sponsor, created = Sponsor.objects.get_or_create(
                    account=self.user,
                    project=project,
                    reward=self.reward,
                    defaults={"amount": self.amount, "status": "paid"},
                )
                if not created:
                    sponsor.amount += self.amount
                    sponsor.status = "paid"
                    sponsor.save()

                # 更新專案的已籌金額
                project.update_raised_amount()

    class Meta:
        ordering = ["-created_at"]
