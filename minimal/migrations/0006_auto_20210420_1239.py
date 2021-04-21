# Generated by Django 3.1 on 2021-04-20 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('minimal', '0005_auto_20210420_0035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='image',
            field=models.ImageField(blank=True, default='default_user_icon.jpeg', null=True, upload_to='', verbose_name='プロフィール画像'),
        ),
        migrations.AlterField(
            model_name='minimalmodel',
            name='obj_image',
            field=models.ImageField(blank=True, default='default_thing_icon.png', null=True, upload_to=''),
        ),
    ]