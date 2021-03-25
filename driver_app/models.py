from django.db import models
from accounts.models import CustomUser
from sponsor_app.models import Sponsor
# Create your models here.

class Driver(models.Model):
  user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
  sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE, default=None, null=True, blank=True)
  is_admin = models.BooleanField(default=False)
  phone = models.CharField(max_length=12)
  qualifications = models.CharField(max_length=500, blank=True)
  name = models.CharField(max_length=25)
  address = models.CharField(max_length=50)
  credits = models.IntegerField(default=0)
  # time in days
  time_with_sponsor = models.IntegerField(default=0)

class Application(models.Model):
    driver = models.ForeignKey(Driver,on_delete=models.CASCADE)
    sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE)
    created_at = models.TimeField(auto_now=False, auto_now_add=True)

