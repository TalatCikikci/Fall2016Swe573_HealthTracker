from django.shortcuts import render

from django.http import HttpResponse
# Create your views here.
def index(request):
    return HttpResponse("Hello World this is the fitster home page!")

def signup(request):
    return HttpResponse("Hello World this is the fitster signup page!")
