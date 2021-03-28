from django.shortcuts import render
from django.http import HttpResponse, JsonResponse 
from rest_framework import viewsets, mixins, generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView 
from .serializers import * 
from django.http.response import JsonResponse
from sponsor_app.models import * 
from driver_app.models import * 
from accounts.models import CustomUser
from rest_framework.response import Response
from django.contrib.auth import authenticate
import requests
import json

class CatalogViewSet(viewsets.ViewSet):
    def list(self,request):
        response = requests.get("https://svcs.ebay.com/services/search/FindingService/v1?SECURITY-APPNAME=ErikBlom-Software-PRD-2dc743efd-8d8e7010&OPERATION-NAME=findItemsByKeywords&SERVICE-VERSION=1.0.0&RESPONSE-DATA-FORMAT=JSON&REST-PAYLOAD&keywords=cat&paginationInput.entriesPerPage=15&GLOBAL-ID=EBAY-US&siteid=0")
        catalog = response.json()
        return Response(catalog)

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
    if request.method == 'POST':
        driver = Driver.objects.get(id=driver_id)
        # check if driver already exists
        serializer = DriverSerializer(driver, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(data=serializer.data,status=200)
        return JsonResponse(data="wrong parameters",status=400)

@api_view(['GET'])
def sponsor_list(request):
    if request.method == 'GET':
        sort_param = request.GET.get('sort','sponsor_name')
        sponsors = Sponsor.objects.all().order_by(sort_param)
        serializer = SponsorSerializer(sponsors, many=True)
        return Response(serializer.data)

@api_view(['GET','POST'])
def driver_list(request):
    if request.method == 'GET':
        drivers = Driver.objects.all()
        serializer = DriverSerializer(drivers, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        data=json.loads(request.body)
        if(not("email" in data and "password" in data)):
            return JsonResponse(data="email/password required",status=400, safe=False)

        # create user associated with the driver
        try:
            user = CustomUser.objects.create_user(email=data['email'], password=data['password'])
        except:
            return JsonResponse(data="User email already taken",status=400, safe=False)

        new_driver = Driver(user=user)
        new_driver.save()
        return JsonResponse(data="Driver Created",status=200, safe=False)

@api_view(['POST'])
def authenticate_driver(request):
    if request.method == 'POST':
        data=json.loads(request.body)
        if('email' not in data or 'password' not in data):
            return JsonResponse(data="Email and password required",status=400, safe=False)
        user = authenticate(username=data['email'], password=data['password'])
        if user is not None:
            driver = Driver.objects.filter(user=user)
            if driver.count() > 0:
                driver = driver.first()
                serializer = DriverSerializer(driver)
                return JsonResponse(serializer.data, status=200)
        return HttpResponse("Unauthorized", status=400)


@api_view(['POST','GET'])
def application(request):
    if request.method == 'POST':
        data=json.loads(request.body)
        if('driver_id' not in data or 'sponsor_id' not in data):
            return JsonResponse(data="driver_id and sponsor_id required",status=400, safe=False)
        # check if application exists
        driver = Driver.objects.filter(id=data["driver_id"])
        sponsor = Sponsor.objects.filter(id=data["sponsor_id"])
        if driver.count() == 0:
            return JsonResponse(data="not a valid driver",status=400, safe=False)
        elif sponsor.count() == 0:
            return JsonResponse(data="not a valid sponsor",status=400, safe=False)
        driver = driver.first()
        sponsor = sponsor.first()
        existing_application = Application.objects.filter(driver=driver,sponsor=sponsor)
        if(existing_application.count() == 0):
            app = Application(driver=driver,sponsor=sponsor)
            app.save()
            return JsonResponse(data="Application submitted",status=200, safe=False)
        else:
            return JsonResponse(data="application already exists",status=400, safe=False)
    if request.method == 'GET':
        apps = Application.objects.all()
        serializer = ApplicationSerializer(apps, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def catalog_search(request,item):
    response = requests.get("https://svcs.ebay.com/services/search/FindingService/v1?SECURITY-APPNAME=ErikBlom-Software-PRD-2dc743efd-8d8e7010&OPERATION-NAME=findItemsByKeywords&SERVICE-VERSION=1.0.0&RESPONSE-DATA-FORMAT=JSON&REST-PAYLOAD&keywords="+item+"&paginationInput.entriesPerPage=15&GLOBAL-ID=EBAY-US&siteid=0")
    catalog = response.json()
    catalog = catalog["findItemsByKeywordsResponse"][0]["searchResult"][0]["item"]
    return Response(catalog)

