from rest_framework import serializers
from sponsor_app.models import Sponsor 
from driver_app.models import Driver

class SponsorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sponsor 
        fields = ('sponsor_name','exchange_rate')
class DriverSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Driver 
        fields = ('name','address','sponsor','phone','credits')
