from rest_framework import serializers
from sponsor_app.models import * 
from driver_app.models import * 

class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor 
        fields = ['id','sponsor_name','exchange_rate']

class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver 
        fields = ['id','name','address','sponsor','phone','credits']

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application 
        fields = ['driver','sponsor','created_at']
