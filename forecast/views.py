from django.shortcuts import render
from django.http import HttpResponse, Http404

# Create your views here.

message = "<h1>We are in the process of building the Luas Forecast app</h1>"

def get_luas_times(request):
    return HttpResponse(message)