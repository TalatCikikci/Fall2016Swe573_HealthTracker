from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext

from .models import Userbasic, Userprofile
from .forms import UserbasicForm, UserprofileForm

# Create your views here.
def index(request):
    return render(request, 'healthtracker/login.html')

def login(request):
    return render(request, 'healthtracker/profile.html')

def signup(request):
    if request.method == "POST":
        bform = UserbasicForm(request.POST, instance=Userbasic())
        pform = UserprofileForm(request.POST, instance=Userprofile())
    else:
        bform = UserbasicForm(instance=Userbasic())
        pform = UserprofileForm(instance=Userprofile())
    return render_to_response(RequestContext(request), 'healthtracker/signup.html', {'userbasic_form':bform, 'userprofile_form':pform})

def registeruser(request):
    return render(request, 'healthtracker/login.html')

def forgottenpassword(request):
    return render(request, 'healthtracker/forgottenpassword.html')

def recoverpassword(request):
    return render(request, 'healthtracker/login.html')
