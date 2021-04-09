from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import requests
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from driver_app.models import *
from .models import *
from api.views import * 

@login_required(login_url='/sponsors/login')
def index(request):
  sponsor_user = Sponsor.objects.filter(user=request.user)
  my_drivers = Driver.objects.filter(sponsor=sponsor_user)
  return render(request = request, template_name = 'sponsor_app/index.html', context={"my_drivers":my_drivers.all()})

def login_view(request):
  # if not logged in already
  if(request.user.is_authenticated == False):
      # check if loggin form was submitted
      form = AuthenticationForm()
      if request.method == 'POST':
        email = request.POST['username']
        password = request.POST['password']
        print(password)
        print(email)
        # first check if the credentials belong to a user
        auth_user = authenticate(request, email=email, password=password)
        print(auth_user)
        # then check if the user is a sponsor user
        if auth_user is None:
            messages.add_message(request, messages.ERROR, 'No account matching the provided credentials')
            return render(request = request, template_name = 'sponsor_app/login.html', context={"form":form})
        elif not Sponsor.objects.filter(user=auth_user):
            messages.add_message(request, messages.ERROR, 'Account not authorized to view the sponsor pages')
            return render(request = request, template_name = 'sponsor_app/login.html', context={"form":form})
        login(request, auth_user)
        template = loader.get_template('sponsor_app/index.html')
        return HttpResponse(template.render())
      # if this is just visiting login page as un logged in user
      else:
       return render(request = request, template_name = 'sponsor_app/login.html', context={"form":form})
  # if already logged in
  else:
    template = loader.get_template('sponsor_app/index.html')
    return HttpResponse(template.render())

@login_required(login_url='/sponsors/login')
def logout_view(request):
  logout(request)
  return login_view(request)

@login_required(login_url='/sponsors/login')
def my_drivers_view(request):
  print(request.user)
  sponsor_user = Sponsor.objects.get(user=request.user)
  my_drivers = Driver.objects.filter(sponsor=sponsor_user)
  return render(request = request, template_name = 'sponsor_app/my_drivers.html', context={"my_drivers":my_drivers})

@login_required(login_url='/sponsors/login')
def home_page(request):
    logoug(request)
    template = loader.get_template('sponsor_app/home.html')
    return HttpResponse(template.render())

@login_required(login_url='/sponsors/login')
def profile_page(request):
    if request.method == 'POST':
        profile_data = request.POST.dict()
        if(profile_data.get("sponsor_name") is not None and len(profile_data.get("sponsor_name"))>0):
            Sponsor.objects.filter(user=request.user).update(sponsor_name=profile_data.get("sponsor_name"))
        if(profile_data.get("exchange_rate") is not None and len(profile_data.get("exchange_rate"))> 0):
            Sponsor.objects.filter(user=request.user).update(exchange_rate=int(profile_data.get("exchange_rate")))
        if(profile_data.get("application_requirements") is not None and len(profile_data.get("application_requirements")) > 0):
            Sponsor.objects.filter(user=request.user).update(application_requirements=profile_data.get("application_requirements"))
        if(profile_data.get("catalog") is not None and len(profile_data.get("catalog")) > 0):
            Sponsor.objects.filter(user=request.user).update(catalog=profile_data.get("catalog"))

        if(profile_data.get("catalog_params") is not None and len(profile_data.get("catalog_params")) > 0):
            Sponsor.objects.filter(user=request.user).update(catalog_params=profile_data.get("catalog_params"))

    sponsor = Sponsor.objects.get(user=request.user)
    return render(request = request, template_name = 'sponsor_app/profile.html', context={"sponsor":sponsor})

@login_required(login_url='/sponsors/login')
def get_drivers_view(request):
    sponsor_user = Sponsor.objects.get(user=request.user)
    if request.method == 'POST':
        application_data = request.POST.dict()
        Driver.objects.filter(id=application_data["new_driver_id"]).update(sponsor=sponsor_user)
        Application.objects.filter(id=application_data["application_id"]).delete()

    my_applications = Application.objects.filter(sponsor=sponsor_user)
    return render(request = request, template_name = 'sponsor_app/get_drivers.html', context={"my_applications":my_applications})

@login_required(login_url='/sponsors/login')
def remove_driver_view(request,id):
    driver_id = id
    if request.method == 'POST':
        Driver.objects.filter(id=driver_id).update(sponsor=None) 
    return my_drivers_view(request)

@login_required(login_url='/sponsors/login')
def edit_driver_view(request,id):
    driver_id = id
    if request.method == 'POST':
        profile_data = request.POST.dict()
        print()
        if(len(profile_data.get("address"))>0):
            print(profile_data.get("address"))
            Driver.objects.filter(id=driver_id).update(address=profile_data.get("address"))
        if(len(profile_data.get("name"))>0):
            Driver.objects.filter(id=driver_id).update(name=profile_data.get("name"))
        if(len(profile_data.get("credits")) > 0):
            print(profile_data.get("credits"))
            Driver.objects.filter(id=driver_id).update(credits=int(profile_data.get("credits")))
    my_driver = Driver.objects.get(id=driver_id)
    return render(request = request, template_name = 'sponsor_app/edit_driver.html',context={"driver":my_driver})

@login_required(login_url='/sponsors/login')
def catalog_view(request):
     search_param = "shoes"
     if request.method == 'POST':
         data = request.POST.dict()
         search_param = data["search_param"]
         print(search_param)
     route = request.build_absolute_uri('/api/')
     catalog = requests.get(route+"catalog/"+search_param)

     if catalog.status_code == 200:
        catalog = catalog.json()
        catalog = catalog['response']
        print(catalog)
     else:
         catalog = []
     return render(request = request, template_name = 'sponsor_app/catalog.html',context={"catalog":catalog})
