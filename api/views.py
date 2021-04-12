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
from django.core import serializers
import requests
import json
import math

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
    if request.method == 'PATCH':
        data = json.loads(request.body)
        updated_driver = Driver.objects.get(id=driver_id)
        if("phone" in data):
            updated_driver.phone = data['phone']
        if("qualifications" in data):
            updated_driver.qualifications = data['qualifications']
        if("name" in data):
            updated_driver.name = data['name']
        if("address" in data):
            updated_driver.address = data['address']
        if("driver_gender" in data and data['driver_gender'] in ["M","F","O"]):
            updated_driver.driver_gender = data['driver_gender']
        if("age" in data):
            updated_driver.age = data['age']
        updated_driver.save()
        serializer = DriverSerializer(updated_driver)
        return JsonResponse(data={"response":serializer.data}, status=200)

@api_view(['GET','POST'])
def sponsor_list(request):
    if request.method == 'GET':
        sort_param = request.GET.get('sort','sponsor_name')
        sponsors = Sponsor.objects.all().order_by(sort_param)
        serializer = SponsorSerializer(sponsors, many=True)
        return Response(data={"response": serializer.data})
    if request.method == 'POST':
        data=json.loads(request.body)
        if(not("email" in data and "password" in data)):
            return JsonResponse(data="email/password required",status=400, safe=False)

        # create user associated with the driver
        try:
            user = CustomUser.objects.create_user(email=data['email'], password=data['password'])
        except:
            return JsonResponse(data="User email already taken",status=400, safe=False)
        
        new_sponsor = Sponsor(user=user)
        if("sponsor_name" in data):
            new_sponsor.sponsor_name = data['sponsor_name']
        if("application_requirements" in data):
            new_sponsor.application_requirements = data['application_requirements']
        if("catalog_params" in data):
            new_sponsor.catalog_params = data['catalog_params']

        new_sponsor.save()
        serializer = SponsorSerializer(new_sponsor)
        return JsonResponse(data={"response": serializer.data},status=200, safe=False)
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
        if("phone" in data):
            new_driver.phone = data['phone']
        if("qualifications" in data):
            new_driver.qualifications = data['qualifications']
        if("name" in data):
            new_driver.name = data['name']
        if("address" in data):
            new_driver.address = data['address']
        if("driver_gender" in data and data['driver_gender'] in ["M","F","O"]):
            new_driver.driver_gender = data['driver_gender']
        if("age" in data):
            new_driver.age = data['age']

        new_driver.save()
        serializer = DriverSerializer(new_driver)
        return JsonResponse(data={"response": serializer.data},status=200, safe=False)

@api_view(['POST'])
def fake_authenticate(request):
    #
    driver = Driver.objects.get(id=1)
    serializer = DriverSerializer(driver)
    return JsonResponse(data={"response":serializer.data}, status=200)

@api_view(['GET'])
def get_catalog_params(request,id):
    if request.method == 'GET':
        sponsor = Sponsor.objects.filter(id=id)
        if sponsor.count() == 0:
            return Response(data={"response": "not a valid sponsor id"}, status=400)
        sponsor = sponsor.first()
        params_string = sponsor.catalog_params
        params_string = params_string.replace(", ",",")
        params_string = params_string.replace(" ,",",")
        params_list = params_string.split(",")

        return Response(data={"response": params_list},status=200)

@api_view(['POST'])
def authenticate_driver(request):
    if request.method == 'POST':
        try:
            data=json.loads(request.body)
        except:
            return JsonResponse(data={"response": "Bad request data"},status=400)
        if('email' not in data or 'password' not in data):
            return JsonResponse(data={"response": "Email and password required"},status=400, safe=False)
        user = authenticate(username=data['email'], password=data['password'])
        if user is not None:
            driver = Driver.objects.filter(user=user)
            if driver.count() > 0:
                driver = driver.first()
                serializer = DriverSerializer(driver)
                return JsonResponse(data={"response": serializer.data}, status=200)
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
            return JsonResponse(data={"response": "not a valid driver"},status=400, safe=False)
        if sponsor.count() == 0:
            return JsonResponse(data={"response": "not a valid sponsor"},status=400, safe=False)
        driver = driver.first()
        sponsor = sponsor.first()
        existing_application = Application.objects.filter(driver=driver,sponsor=sponsor)
        if(existing_application.count() == 0):
            app = Application(driver=driver,sponsor=sponsor)
            app.save()
            return JsonResponse(data={"response": "Application submitted"},status=200, safe=False)
        else:
            return JsonResponse(data={"response": "Application already exists"},status=400, safe=False)
    if request.method == 'GET':
        apps = Application.objects.all()
        serializer = ApplicationSerializer(apps, many=True)
        return Response(data={"response": serializer.data})

@api_view(['POST'])
def purchase_item(request):
    if request.method == 'POST':
        data=json.loads(request.body)
        if('driver_id' not in data or 'item_id' not in data or 'cost' not in data):
            return JsonResponse(data="driver_id, sponsor_id, and cost are required",status=400, safe=False)

        # check if application exists
        driver = Driver.objects.filter(id=data["driver_id"])
        if driver.count() == 0:
            return JsonResponse(data={"response": "not a valid driver"},status=400, safe=False)
       
        # check if driver has a sponsor 
        driver = driver.first()
        sponsor = Sponsor.objects.filter(id=driver.sponsor.id)
        if sponsor.count() == 0:
            return JsonResponse(data={"response": "driver has no sponsor"},status=400, safe=False)
        sponsor = sponsor.first()

        # check if driver can afford item
        available_credits = driver.credits
        # convert item cost from string to float and then into 
        # number of credits based on exchange rate rounded up
        item_cost = math.ceil((sponsor.exchange_rate)*float(data['cost']))

        if(item_cost > available_credits): 
            return JsonResponse(data={"response": "driver doesn't have enough credits"},status=400, safe=False)
        else:
            driver.credits = available_credits-item_cost
            new_purchase = Purchases(driver=driver,cost=data['cost'],item_id=data['item_id'])
            driver.save()
            new_purchase.save()
            return JsonResponse(data={"response": "purchases item"},status=200, safe=False)

@api_view(['GET'])
def catalog_search(request,item):
    response = requests.get("https://svcs.ebay.com/services/search/FindingService/v1?SECURITY-APPNAME=ErikBlom-Software-PRD-2dc743efd-8d8e7010&OPERATION-NAME=findItemsByKeywords&SERVICE-VERSION=1.0.0&RESPONSE-DATA-FORMAT=JSON&REST-PAYLOAD&keywords="+item+"&paginationInput.entriesPerPage=15&GLOBAL-ID=EBAY-US&siteid=0")
    raw_catalog = response.json()
    raw_catalog = raw_catalog["findItemsByKeywordsResponse"][0]["searchResult"][0]["item"]
    refined_catalog = [None] * len(raw_catalog)

    for i in range(len(raw_catalog)):
        c = raw_catalog[i]
        r = {"name": c['title'][0], "id": c['itemId'][0], "imageURL":c['galleryURL'][0], "price":c['sellingStatus'][0]['currentPrice'][0]['__value__'], "location": c['location'][0]}
        refined_catalog[i] = r
    return Response({"response": refined_catalog})

