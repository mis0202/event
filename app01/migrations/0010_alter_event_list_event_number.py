# Generated by Django 3.2 on 2023-07-02 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0009_alter_event_list_things_type1'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event_list',
            name='event_number',
            field=models.CharField(max_length=32, verbose_name='工单编号'),
        ),
    ]