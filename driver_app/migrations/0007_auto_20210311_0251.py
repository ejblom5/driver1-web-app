# Generated by Django 4.0 on 2021-03-11 02:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sponsor_app', '0003_auto_20210219_0349'),
        ('driver_app', '0006_driver_is_admin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='driver',
            name='address',
        ),
        migrations.AlterField(
            model_name='driver',
            name='sponsor',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='sponsor_app.sponsor'),
        ),
    ]
