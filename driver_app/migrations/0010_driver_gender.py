# Generated by Django 3.1.6 on 2021-04-07 03:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('driver_app', '0009_auto_20210402_1123'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='gender',
            field=models.CharField(default='O', max_length=1),
        ),
    ]
