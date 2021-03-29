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
  sponsor_user = Sponsor.objects.get(user=request.user)
  my_drivers = Driver.objects.filter(sponsor=sponsor_user)
  return render(request = request, template_name = 'admin_app/index.html', context={"my_drivers":my_drivers})

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
        admin = Driver.objects.filter(user=auth_user,is_admin=True)
        if auth_user is None:
            messages.add_message(request, messages.ERROR, 'No account matching the provided credentials')
            return render(request = request, template_name = 'admin_app/login.html', context={"form":form})
        elif not admin:
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
  my_drivers = Driver.objects.filter(sponsor=request.user.sponsor)
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
        for i in catalog:
            i["galleryURL"] = i["galleryURL"][0]
            i["title"] = i["title"][0]
            i["price"] = i["sellingStatus"][0]["currentPrice"][0]["__value__"]
     else:
         catalog = []
     return render(request = request, template_name = 'admin_app/catalog.html',context={"catalog":catalog})

@login_required(login_url='/admins/login')
def profile_page(request):
    if request.method == 'POST':
        profile_data = request.POST.dict()
<<<<<<< HEAD
        if(len(profile_data.get("name"))>0):
            Driver.objects.filter(user=request.user).update(sponsor_name=profile_data.get("sponsor_name"))
=======
        if(profile_data.get("name") != None and len(profile_data.get("name"))>0):
            Driver.objects.filter(user=request.user).update(name=profile_data.get("name"))
>>>>>>> 043b37aee022400a417ecc27af78577104bc96b0

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

from django.contrib import admin
from django.urls import path, include, re_path
from two_factor.admin import AdminSiteOTPRequired
from two_factor.urls import urlpatterns as tf_urls

from django.conf import settings
from django.http import  HttpResponseRedirect
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import resolve_url
from django.urls import reverse
from django.utils.http import is_safe_url
from two_factor.admin import AdminSiteOTPRequired, AdminSiteOTPRequiredMixin


class AdminSiteOTPRequiredMixinRedirSetup(AdminSiteOTPRequired):
    def login(self, request, extra_context=None):
        redirect_to = request.POST.get(
            REDIRECT_FIELD_NAME, request.GET.get(REDIRECT_FIELD_NAME)
        )
        # For users not yet verified the AdminSiteOTPRequired.has_permission
        # will fail. So use the standard admin has_permission check:
        # (is_active and is_staff) and then check for verification.
        # Go to index if they pass, otherwise make them setup OTP device.
        if request.method == "GET" and super(
            AdminSiteOTPRequiredMixin, self
        ).has_permission(request):
            # Already logged-in and verified by OTP
            if request.user.is_verified():
                # User has permission
                index_path = reverse("admin:index", current_app=self.name)
            else:
                # User has permission but no OTP set:
                index_path = reverse("two_factor:setup", current_app=self.name)
            return HttpResponseRedirect(index_path)

        if not redirect_to or not is_safe_url(
            url=redirect_to, allowed_hosts=[request.get_host()]
        ):
            redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

        return redirect_to_login(redirect_to)
