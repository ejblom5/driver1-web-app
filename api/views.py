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
from django.contrib.auth import authenticate
from driver_app.models import *
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

@api_view(['GET','PATCH'])
def driver_detail(request,id):
    driver_id = id
    if request.method == 'GET':
        drivers = Driver.objects.get(id=driver_id)
        serializer = DriverSerializer(drivers)
        return Response(serializer.data)
    if request.method == 'PATCH':
        driver = Driver.objects.get(id=driver_id)
        serializer = DriverSerializer(driver, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(data=serializer.data,status=200)
        return JsonResponse(data="wrong parameters",status=400)

@api_view(['GET','POST'])
def driver_list(request):
    if request.method == 'GET':
        drivers = Driver.objects.all()
        serializer = DriverSerializer(drivers, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        data = request.data
        print(data)
        print(request.data)
        if(not("email" in data and "password" in data)):
            return JsonResponse(data="email/password required",status=400, safe=False)

        # create user associated with the driver
        try:
            user = CustomUser.objects.create_user(email=data['email'], password=data['password'])
        except:
            return JsonResponse(data="User email already taken",status=400, safe=False)

        request.data['user'] = user.id
        data.pop('email')

        serializer = DriverSerializer(data=request.data)
        if serializer.is_valid():
            serializer.create()
            serializer.save()
            return JsonResponse(data=serializer.data,status=200,safe=False)
        return JsonResponse(data="wrong parameters",status=400, safe=False)

@api_view(['POST'])
def authenticate_driver(request):
    user = authenticate(username=request.data['email'], password=request.data['password'])
    if user:
        driver = Driver.objects.filter(user=user.id)
        if driver:
            serializer = DriverSerializer(driver)
            return Response(serializer.data)
    return HttpResponse('Unauthorized', status=401)

@api_view(['GET'])
def catalog_search(request,item):
    response = requests.get("https://svcs.ebay.com/services/search/FindingService/v1?SECURITY-APPNAME=ErikBlom-Software-PRD-2dc743efd-8d8e7010&OPERATION-NAME=findItemsByKeywords&SERVICE-VERSION=1.0.0&RESPONSE-DATA-FORMAT=JSON&REST-PAYLOAD&keywords="+item+"&paginationInput.entriesPerPage=15&GLOBAL-ID=EBAY-US&siteid=0")
    catalog = response.json()
    catalog = catalog["findItemsByKeywordsResponse"][0]["searchResult"][0]["item"]
    return Response(catalog)

