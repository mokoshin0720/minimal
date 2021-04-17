from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

# Create your models here.
class CustomUser(AbstractUser):
    age = models.IntegerField(null=True)

class ThingStatus(models.Model):
    name = models.CharField('物の状況', max_length=50)
    
    def __str__(self):
        return self.name

class MinimalModel(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    buy_reason = models.TextField()
    sell_reason = models.TextField(null=True, blank=True)
    status = models.ForeignKey(ThingStatus, verbose_name='物の状況', on_delete=models.PROTECT)
    obj_image = models.ImageField(upload_to='')
    buy_date = models.DateField()
    buy_price = models.IntegerField()
    sell_price = models.IntegerField(null=True, blank=True)
    nice_throw = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title