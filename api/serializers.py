from rest_framework import serializers
from sponsor_app.models import Sponsor 

class SponsorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sponsor 
        fields = ('sponsor_name','exchange_rate')
