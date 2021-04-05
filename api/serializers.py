from rest_framework import serializers
from sponsor_app.models import * 
from driver_app.models import * 

class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor 
        fields = ['id','sponsor_name','exchange_rate', 'application_requirements']

class DriverSerializer(serializers.ModelSerializer):
    #sponsor = SponsorSerializer(read_only = True)
    class Meta:
        model = Driver 
        fields = ['id','name','address','sponsor','phone','credits','gender']
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name',instance.name)
        instance.address = validated_data.get('address',instance.address)
        instance.name = validated_data.get('name',instance.name)

class ApplicationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    class Meta:
        model = Application 
        fields = ['driver','sponsor','created_at']
