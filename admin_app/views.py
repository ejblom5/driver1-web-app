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

@login_required(login_url='/admins/login')
def index(request):
  admin_user = Driver.objects.filter(user=request.user,is_admin=True)
  if admin_user.count() == 0:
    logout(request)
    return login_view(request)
  admin_user = admin_user.first()
  sponsor_user =  admin_user.sponsor 
  my_drivers = Driver.objects.filter(sponsor=sponsor_user)
  return render(request = request, template_name = 'admin_app/index.html', context={"driver_count":my_drivers.count(),"admin":admin_user,"sponsor":sponsor_user})

def login_view(request):
  # if not logged in already
  if(request.user.is_authenticated == False):
      # check if loggin form was submitted
      form = AuthenticationForm()
      if request.method == 'POST':
        email = request.POST['username']
        password = request.POST['password']

        # first check if the credentials belong to a user
        auth_user = authenticate(request, email=email, password=password)
        # then check if the user is a sponsor user
        admin = Driver.objects.filter(user=auth_user,is_admin=True)
        if auth_user is None:
            messages.add_message(request, messages.ERROR, 'No account matching the provided credentials')
            return render(request = request, template_name = 'admin_app/login.html', context={"form":form})
        elif admin.count() == 0:
            messages.add_message(request, messages.ERROR, 'Account not authorized to view the admin pages')
            return render(request = request, template_name = 'admin_app/login.html', context={"form":form})
        login(request, auth_user)
        template = loader.get_template('admin_app/index.html')
        return HttpResponse(template.render())
      # if this is just visiting login page as un logged in user
      else:
       return render(request = request, template_name = 'admin_app/login.html', context={"form":form})
  # if already logged in
  else:
    template = loader.get_template('admin_app/index.html')
    return HttpResponse(template.render())

@login_required(login_url='/admins/login')
def logout_view(request):
  logout(request)
  return login_view(request)

@login_required(login_url='/admins/login')
def my_drivers_view(request):
  admin_user = Driver.objects.filter(user=request.user).first()
  my_drivers = Driver.objects.filter(sponsor=admin_user.sponsor)
  return render(request = request, template_name = 'admin_app/my_drivers.html', context={"my_drivers":my_drivers})

@login_required(login_url='/admins/login')
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
     else:
         catalog = []
     return render(request = request, template_name = 'admin_app/catalog.html',context={"catalog":catalog})

@login_required(login_url='/admins/login')
def profile_page(request):
    if request.method == 'POST':
        profile_data = request.POST.dict()
        if(profile_data.get("name") != None and len(profile_data.get("name"))>0):
            Driver.objects.filter(user=request.user).update(name=profile_data.get("name"))

    admin = Driver.objects.get(user=request.user)
    return render(request = request, template_name = 'admin_app/profile.html', context={"admin":admin})

@login_required(login_url='/admins/login')
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
    return render(request = request, template_name = 'admin_app/edit_driver.html',context={"driver":my_driver})
