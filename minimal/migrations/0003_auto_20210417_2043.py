# Generated by Django 3.1 on 2021-04-17 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('minimal', '0002_auto_20210417_1913'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='age',
        ),
        migrations.AddField(
            model_name='customuser',
            name='image',
            field=models.ImageField(default='media/zebra0.jpg', upload_to='', verbose_name='プロフィール画像'),
        ),
    ]
