from django.shortcuts import render

from django.http import HttpResponse
# Create your views here.
def index(request):
    return render(request, 'healthtracker/login.html')

def login(request):
    return render(request, 'healthtracker/profile.html')

def signup(request):
    return render(request, 'healthtracker/signup.html')

def registeruser(request):
    return render(request, 'healthtracker/login.html')

def forgottenpassword(request):
    return render(request, 'healthtracker/forgottenpassword.html')
