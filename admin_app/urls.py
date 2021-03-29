from django.urls import path
from . import views
#2fa
from two_factor.admin import AdminSiteOTPRequired
from two_factor.urls import urlpatterns as tf_urls

from django.conf import settings
from django.http import  HttpResponseRedirect
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import resolve_url
from django.urls import reverse
from django.utils.http import is_safe_url



app_name = 'admin_app'


urlpatterns = [
  path('admin/', views.AdminSiteOTPRequiredMixinRedirSetup),
  path('', views.include(tf_urls, "two_factor")),
  path('',views.index, name='index'),
  path('login',views.login_view, name='login'),
  path('logout',views.logout_view, name='logout'),
  path('my_drivers',views.my_drivers_view, name='my drivers'),
  path('edit_driver/<int:id>',views.edit_driver_view, name='my drivers'),
  path('profile',views.profile_page, name='profile'),
  path('catalog',views.catalog_view, name='catalog'),
  
]
