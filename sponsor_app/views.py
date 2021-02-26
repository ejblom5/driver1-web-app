from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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
  return index(request)
