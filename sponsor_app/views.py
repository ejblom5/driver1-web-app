from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from driver_app.models import *
from .models import *

@login_required(login_url='/sponsors/login')
def index(request):
  template = loader.get_template('sponsor_app/index.html')
  return HttpResponse(template.render())

def login_view(request):
  auth_user = None
  sponsor_user = None
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']

    # first check if the credentials belong to a user
    auth_user = authenticate(request, username=username, password=password)
    # then check if the user is a sponsor user
    sponsor_user = Sponsor.objects.filter(user=auth_user)

  if auth_user is not None and sponsor_user is not None:
    login(request, auth_user)
    template = loader.get_template('sponsor_app/index.html')
    return HttpResponse(template.render())
  else:
    messages.add_message(request, messages.ERROR, 'Failed to login')
    form = AuthenticationForm()
    return render(request = request, template_name = 'sponsor_app/login.html', context={"form":form})

def logout_view(request):
  logout(request)
  return login_view(request)

def my_drivers_view(request):
  sponsor_user = Sponsor.objects.get(user=request.user)
  my_drivers = Driver.objects.filter(sponsor=sponsor_user)
  return render(request = request, template_name = 'sponsor_app/my_drivers.html', context={"my_drivers":my_drivers})

def home_page(request):
    template = loader.get_template('sponsor_app/home.html')
    return HttpResponse(template.render())

def profile_page(request):
    if request.method == 'POST':
        profile_data = request.POST.dict()
        if(len(profile_data.get("sponsor_name"))>0):
            Sponsor.objects.filter(user=request.user).update(sponsor_name=profile_data.get("sponsor_name"))
        if(len(profile_data.get("exchange_rate"))> 0):
                Sponsor.objects.filter(user=request.user).update(exchange_rate=int(profile_data.get("exchange_rate")))

    sponsor = Sponsor.objects.get(user=request.user)
    return render(request = request, template_name = 'sponsor_app/profile.html', context={"sponsor":sponsor})

def get_drivers_view(request):
    sponsor_user = Sponsor.objects.get(user=request.user)
    if request.method == 'POST':
        application_data = request.POST.dict()
        Driver.objects.filter(id=application_data["new_driver_id"]).update(sponsor=sponsor_user)
        Application.objects.filter(id=application_data["application_id"]).delete()

    my_applications = Application.objects.filter(sponsor=sponsor_user)
    return render(request = request, template_name = 'sponsor_app/get_drivers.html', context={"my_applications":my_applications})

