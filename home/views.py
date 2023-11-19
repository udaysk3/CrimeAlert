from django.shortcuts import render,redirect
from django.http import HttpResponse
from . import models

# Create your views here.
def home(request):
    return render(request,'index.html')

