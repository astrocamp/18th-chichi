from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Project(models.Model):
    STATUS_CHOICES = [
        ('pending', '待上架'),
        ('live', '已上架'),
        ('ended', '已下架'),
    ]
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100,null=True)
    cover_image = models.FileField(upload_to="uploads/" ,null=True)
    raised_amount = models.DecimalField(null=True ,decimal_places= 0 , max_digits=10)
    goal_amount = models.DecimalField(decimal_places= 0 , max_digits=10)
    start_at = models.DateTimeField(null=True)
    end_at = models.DateTimeField()
    story = models.TextField()
    location = models.CharField(null=True,max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(null=True)
    account = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
    )

    collect_account = models.ManyToManyField(
        User,
        related_name="collect_projects",
        through="CollectProject",
        through_fields=("project","account"),
    )
    def update_status(self):
        """
        更新專案狀態：根據時間設定自動上架或下架
        """
        current_time = now()
        if self.status == 'pending' and self.start_at and current_time >= self.start_at:
            self.status = 'live'
            self.save()
        elif self.status == 'live' and self.end_at and current_time >= self.end_at:
            self.status = 'ended'
            self.save()

class CollectProject(models.Model):
    account = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)


    

    
   
