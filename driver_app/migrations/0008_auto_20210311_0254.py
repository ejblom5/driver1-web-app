# Generated by Django 4.0 on 2021-03-11 02:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('driver_app', '0007_auto_20210311_0251'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='driver',
            name='email',
        ),
        migrations.AddField(
            model_name='driver',
            name='address',
            field=models.CharField(default='none', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='driver',
            name='qualifications',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
