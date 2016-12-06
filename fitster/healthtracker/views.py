from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User, BaseUserManager, AbstractBaseUser
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .models import Userprofile
from .forms import UserForm, UserprofileForm
from .utils import UserUtils
import healthtracker.signals as signals


# Create your views here.
def index(request):
    return render(request,
                  'healthtracker/login.html'
                  )


def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        # Using "login" here clashes with the view named "login" so we use "auth_login" instead.
        auth_login(request, user)
        return redirect('/healthtracker/profile')
    else:
        return redirect('/healthtracker')


def logout(request):
    # Using "logout" here clashes with the view named "logout" so we use "auth_logout" instead.
    auth_logout(request)
    return redirect('/healthtracker')


def signup(request):
    if request.method == "POST":
        uform = UserForm(request.POST, instance=User())
        pform = UserprofileForm(request.POST, instance=Userprofile())

        if uform.is_valid() and pform.is_valid():
            email = BaseUserManager.normalize_email(uform.cleaned_data['email'])
            djangouser = User.objects.create_user(uform.cleaned_data['username'],
                                     email,
                                     uform.cleaned_data['password'])
            djangouser.last_name = uform.cleaned_data['last_name']
            djangouser.first_name = uform.cleaned_data['first_name']
            
            djangouser._dateofbirth = pform.cleaned_data['dateofbirth']
            djangouser._gender = pform.cleaned_data['gender']
            djangouser._height = pform.cleaned_data['height']
            djangouser._weight = pform.cleaned_data['weight']

            if pform.cleaned_data['notes']:
                djangouser._notes = pform.cleaned_data['notes']
            else:
                djangouser._notes = ''

            signals.user_initiated.send(sender=None, instance=djangouser,
                                dateofbirth=djangouser._dateofbirth,
                                gender=djangouser._gender,
                                height=djangouser._height,
                                weight=djangouser._weight,
                                notes=djangouser._notes)
            
            djangouser.save()
            return HttpResponseRedirect('..')
    else:
        uform = UserForm(instance=User())
        pform = UserprofileForm(instance=Userprofile())
    return render(request,
                  'healthtracker/signup.html',
                  {'user_form':uform, 'userprofile_form':pform}
                  )


@login_required
def profile(request):
    return render(request, 'healthtracker/profile.html')


def editprofile(request):
    return render(request, 'healthtracker/editprofile.html')


def forgottenpassword(request):
    return render(request, 'healthtracker/forgottenpassword.html')


def recoverpassword(request):
    return redirect('/healthtracker')
