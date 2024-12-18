from django.db import models
import datetime

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

