from django.db import models
from django.core.validators import MinValueValidator


class Pledges(models.Model):
    payment_status_choices = [
        ("PENDING", "待付款"),
        ("PAID", "已付款"),
        ("FAILED", "付款失敗"),
        ("REFUNDED", "已退款"),
    ]
    pledges_amount = models.DecimalField(decimal_places=0, max_digits=10)
    pledges_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=10, choices=payment_status_choices, default="PENDING"
    )
