from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def courses(request):
    return HttpResponse ("this is first app courses page")
def home(request):
    return HttpResponse ("this is first app home page")
def about(request):
    return HttpResponse ("this is first app about page")