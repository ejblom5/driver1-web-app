# Generated by Django 4.0 on 2021-02-09 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sponsor_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsor',
            name='account_id',
            field=models.IntegerField(default=0),
        ),
    ]