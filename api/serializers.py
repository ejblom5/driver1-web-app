from rest_framework import serializers
from sponsor_app.models import Sponsor 
from driver_app.models import Driver

class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor 
        fields = ['sponsor_name','exchange_rate']

class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver 
        fields = ['name','address','sponsor','phone','credits','email']
