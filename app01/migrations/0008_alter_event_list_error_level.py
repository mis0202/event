# Generated by Django 3.2 on 2023-07-01 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0007_auto_20230627_2317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event_list',
            name='error_level',
            field=models.SmallIntegerField(choices=[(0, '不涉及'), (1, '一级故障'), (2, '二级故障'), (3, '三级故障'), (4, '四级故障')], verbose_name='故障等级'),
        ),
    ]