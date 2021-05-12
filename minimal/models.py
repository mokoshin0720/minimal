from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.utils import timezone

# Create your models here.
class CustomUser(AbstractUser):
    image = models.ImageField(upload_to='', blank=True, null=True, verbose_name='プロフィール画像', default='default_user_icon.jpeg')

class ThingStatus(models.Model):
    name = models.CharField('物の状況', max_length=50)
    
    def __str__(self):
        return self.name

class MinimalModel(models.Model):
    title = models.CharField(max_length=20, verbose_name='品物名')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='購入者')
    buy_reason = models.TextField(verbose_name='購入した理由')
    sell_reason = models.TextField(null=True, blank=True, verbose_name='手放す理由')
    status = models.ForeignKey(ThingStatus, on_delete=models.PROTECT, verbose_name='物の状況', default=1)
    obj_image = models.ImageField(upload_to='', blank=True, null=True, default='default_thing_icon.png', verbose_name='物の画像')
    buy_date = models.DateField(verbose_name='購入日')
    buy_price = models.PositiveIntegerField(verbose_name='購入金額')
    sell_price = models.IntegerField(null=True, blank=True, verbose_name='売却金額')
    nice_throw = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Like(models.Model):
    thing = models.ForeignKey(MinimalModel, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    timestamp = models.DateField(default=timezone.now)

    def __str__(self):
        return str(self.thing.id)