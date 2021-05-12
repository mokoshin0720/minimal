# Generated by Django 3.1 on 2021-05-11 16:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('minimal', '0009_auto_20210503_2349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='minimalmodel',
            name='buy_price',
            field=models.PositiveIntegerField(verbose_name='購入金額'),
        ),
        migrations.AlterField(
            model_name='minimalmodel',
            name='status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='minimal.thingstatus', verbose_name='物の状況'),
        ),
    ]
