from django.shortcuts import render
from django.http import HttpResponse, JsonResponse 
from rest_framework import viewsets, mixins, generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView 
from .serializers import SponsorSerializer, DriverSerializer 
from django.http.response import JsonResponse
from sponsor_app.models import Sponsor 
from driver_app.models import Driver 
from accounts.models import CustomUser
from rest_framework.response import Response
import requests

class CatalogViewSet(viewsets.ViewSet):
    def list(self,request):
        response = requests.get("https://svcs.ebay.com/services/search/FindingService/v1?SECURITY-APPNAME=ErikBlom-Software-PRD-2dc743efd-8d8e7010&OPERATION-NAME=findItemsByKeywords&SERVICE-VERSION=1.0.0&RESPONSE-DATA-FORMAT=JSON&REST-PAYLOAD&keywords=cat&paginationInput.entriesPerPage=15&GLOBAL-ID=EBAY-US&siteid=0")
        catalog = response.json()
        return Response(catalog)

class SponsorList(generics.ListAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer 

class SponsorDetail(generics.RetrieveAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer 

class DriverDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer

@api_view(['GET','POST'])
def driver_list(request):
    if request.method == 'GET':
        drivers = Driver.objects.all()
        serializer = DriverSerializer(drivers, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        user = CustomUser.objects.create_user(email=request.data['email'],
                                password='pass')
        request.data['user'] = user.id 

        drivers = Driver.objects.all()
        serializer = DriverSerializer(drivers, many=True)
        return Response(serializer.data)
