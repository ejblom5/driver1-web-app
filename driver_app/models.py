from django.db import models
from accounts.models import CustomUser
from sponsor_app.models import Sponsor
# Create your models here.

class Driver(models.Model):
  user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
  sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE)
  phone = models.CharField(max_length=12)
  qualifications = models.CharField(max_length=500)
  name = models.CharField(max_length=25)
  address = models.CharField(max_length=100)
  credits = models.IntegerField(default=0)
  # time in days
  time_with_sponsor = models.IntegerField(default=0)
