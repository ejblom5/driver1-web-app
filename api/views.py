from django.shortcuts import render
from rest_framework import viewsets
from .serializers import SponsorSerializer, DriverSerializer 
from sponsor_app.models import Sponsor 
from driver_app.models import Driver 

# Create your views here.

class SponsorViewSet(viewsets.ModelViewSet):
    queryset = Sponsor.objects.all().order_by('sponsor_name')
    serializer_class = SponsorSerializer 
class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all().order_by('name')
    serializer_class = DriverSerializer 
