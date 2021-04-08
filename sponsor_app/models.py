from django.db import models
from accounts.models import CustomUser
# Create your models here.

class Sponsor(models.Model):
  user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
  sponsor_name = models.CharField(max_length=20)
  exchange_rate = models.IntegerField(default=1)
  catalog = models.CharField(max_length=100)
  catalog_key = models.CharField(max_length=100)
  catalog_params = models.CharField(max_length=200)
  application_requirements = models.CharField(max_length=600)
