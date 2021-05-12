# Generated by Django 3.1 on 2021-05-11 17:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('minimal', '0010_auto_20210512_0142'),
    ]

    operations = [
        migrations.AddField(
            model_name='minimalmodel',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='minimalmodel',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]