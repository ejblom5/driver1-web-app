# Generated by Django 3.1.6 on 2021-03-26 16:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('driver_app', '0009_auto_20210326_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='driver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='driver_app.driver'),
        ),
    ]