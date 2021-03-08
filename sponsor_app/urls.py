from django.urls import path
from . import views

app_name = 'sponsor_app'
urlpatterns = [
  path('',views.index, name='index'),
  path('login',views.login_view, name='login'),
  path('logout',views.logout_view, name='logout'),
  path('my_drivers',views.my_drivers_view, name='my drivers'),
  path('profile',views.profile_page, name='profile'),
  path('get_drivers',views.get_drivers_view, name='get drivers'),
  path('edit_driver/<int:id>',views.edit_driver_view, name='get drivers'),
  path('catalog',views.catalog_view, name='catalog'),
]
