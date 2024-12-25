from django.db import models

class Order(models.Model):
    order_id = models.CharField(max_length=100, unique=True)
    amount = models.IntegerField()
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Order {self.order_id}"