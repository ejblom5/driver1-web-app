from django.urls import path
from . import views

app_name = 'home_app'
urlpatterns = [
  path('',views.home_view, name='home'),
  path('team',views.team_view, name='team'),
]
