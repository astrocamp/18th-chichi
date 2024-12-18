from django.db import models

class Project(models.Model):
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