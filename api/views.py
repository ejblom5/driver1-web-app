from django.shortcuts import render
from rest_framework import viewsets
from .serializers import SponsorSerializer 
from sponsor_app.models import Sponsor 
# Create your views here.

class SponsorViewSet(viewsets.ModelViewSet):
    queryset = Sponsor.objects.all().order_by('sponsor_name')
    serializer_class = SponsorSerializer 
