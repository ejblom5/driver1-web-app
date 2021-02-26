# Generated by Django 4.0 on 2021-02-24 15:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sponsor_app', '0003_auto_20210219_0349'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=12)),
                ('qualifications', models.CharField(max_length=500)),
                ('name', models.CharField(max_length=25)),
                ('address', models.CharField(max_length=100)),
                ('credits', models.IntegerField(default=0)),
                ('time_with_sponsor', models.IntegerField(default=0)),
                ('sponsor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sponsor_app.sponsor')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
