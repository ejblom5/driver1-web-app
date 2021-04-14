from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import requests
from django.contrib import messages

def home_view(request):
    template = loader.get_template('home_app/home.html')
    return HttpResponse(template.render())

def team_view(request):
    template = loader.get_template('home_app/team.html')
    return HttpResponse(template.render())
