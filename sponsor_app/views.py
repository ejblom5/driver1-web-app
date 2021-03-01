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
  # if not logged in already
  if(request.user.is_authenticated == False):
      # check if loggin form was submitted
      form = AuthenticationForm()
      if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # first check if the credentials belong to a user
        auth_user = authenticate(request, username=username, password=password)
        # then check if the user is a sponsor user
        sponsor_user = Sponsor.objects.filter(user=auth_user)
        if auth_user is None:
            messages.add_message(request, messages.ERROR, 'No account matching the provided credentials')
            return render(request = request, template_name = 'sponsor_app/login.html', context={"form":form})
        elif not sponsor_user:
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
  sponsor_user = Sponsor.objects.get(user=request.user)
  my_drivers = Driver.objects.filter(sponsor=sponsor_user)
  return render(request = request, template_name = 'sponsor_app/my_drivers.html', context={"my_drivers":my_drivers})

@login_required(login_url='/sponsors/login')
def home_page(request):
    template = loader.get_template('sponsor_app/home.html')
    return HttpResponse(template.render())

@login_required(login_url='/sponsors/login')
def profile_page(request):
    if request.method == 'POST':
        profile_data = request.POST.dict()
        if(len(profile_data.get("sponsor_name"))>0):
            Sponsor.objects.filter(user=request.user).update(sponsor_name=profile_data.get("sponsor_name"))
        if(len(profile_data.get("exchange_rate"))> 0):
                Sponsor.objects.filter(user=request.user).update(exchange_rate=int(profile_data.get("exchange_rate")))

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
def edit_driver_view(request,id):
    driver_id = id
    my_driver = Driver.objects.get(id=driver_id) 
    return render(request = request, template_name = 'sponsor_app/edit_driver.html',context={"driver":my_driver})

