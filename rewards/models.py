from django.db import models
from projects.views import Project
import datetime
from autoslug import AutoSlugField
import random
import string


def generate_random_slug():
    # 生成 8 位隨機字母數字組合
    letters_and_digits = string.ascii_lowercase + string.digits
    return "".join(random.choice(letters_and_digits) for i in range(8))


def default_delivery_date():
    return datetime.date.today() + datetime.timedelta(days=7)

class Reward(models.Model):
    title = models.CharField(max_length=300)  
    description = models.TextField(blank=True)  
    price = models.DecimalField(default=0, max_digits=10, decimal_places=0)  
    estimated_delivery = models.DateField(default=default_delivery_date) 
    quantity = models.PositiveIntegerField(default=1)  
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(null=True)
    deleted_at= models.DateTimeField(null=True,db_index=True)
    project = models.ForeignKey(Project,on_delete=models.CASCADE)


    def __str__(self):
        return self.title
    
class RewardProduct(models.Model):
    name = models.CharField(max_length=300)
    rewards = models.ManyToManyField(Reward ,blank=True)
    project = models.ForeignKey(Project,on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.name} (x{self.quantity})"

class OptionalAdd(models.Model):
    name = models.CharField(max_length=300)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=0)
    rewards = models.ManyToManyField(Reward, blank=True)
    project = models.ForeignKey(Project,on_delete=models.CASCADE)


    def __str__(self):
        return self.name
