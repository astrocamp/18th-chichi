from django.db import models, transaction
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
        with transaction.atomic():
            # 檢查訂單狀態是否改變
            if self.pk:
                old_order = Order.objects.get(pk=self.pk)
                status_changed = old_order.paid != self.paid
            else:
                status_changed = self.paid

            # 保存訂單
            super().save(*args, **kwargs)

            # 只在支付狀態改變且為已支付時更新
            if status_changed and self.paid:
                # 確定專案
                project = self.reward.project if self.reward else None
                if not project and self.reward is None:
                    # 如果是自由贊助，從 description 中取得專案標題
                    from projects.models import Project

                    project_title = self.description.split(" - ")[0]
                    project = Project.objects.filter(title=project_title).first()

                if project:
                    # 更新 Sponsor 記錄的狀態
                    from projects.models import Sponsor

                    # 找到所有符合條件的待付款記錄並更新
                    Sponsor.objects.filter(
                        account=self.user,
                        project=project,
                        reward=self.reward,
                        amount=self.amount,
                        status="pending",
                    ).update(status="paid")

                    # 更新專案的已籌金額
                    project.update_raised_amount()

    class Meta:
        ordering = ["-created_at"]
