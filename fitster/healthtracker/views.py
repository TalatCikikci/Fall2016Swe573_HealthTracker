from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User, BaseUserManager, AbstractBaseUser
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import logging

from .models import Userprofile
from .forms import UserForm, UserprofileForm
from .utils import UserUtils, ApiWrapper
import healthtracker.signals as signals


logger = logging.getLogger('django')

# Create your views here.
def index(request):
    return render(request,
                  'healthtracker/login.html'
                  )


def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    
    logger.info("Login request as" +
                    "\n\tUsername: " + username
                )
    
    user = authenticate(username=username, password=password)
    if user is not None:
        # Using "login" here clashes with the view named "login" so we use "auth_login" instead.
        auth_login(request, user)
        
        logger.info("User succesfully logged in as " + user.username)
        
        return redirect('/healthtracker/profile')
    else:
        
        logger.info("User authentication failed with given credentials!")
        
        return redirect('/healthtracker')


def logout(request):
    logger.info("Logging out...")
    # Using "logout" here clashes with the view named "logout" so we use "auth_logout" instead.
    auth_logout(request)
    logger.info("User " + request.user.username + " logged out.")
    return redirect('/healthtracker')


def signup(request):
    if request.method == "POST":
        logger.info("Processing signup request...")
        uform = UserForm(request.POST, instance=User())
        pform = UserprofileForm(request.POST, instance=Userprofile())

        logger.info("New signup request.")

        if uform.is_valid() and pform.is_valid():
            email = BaseUserManager.normalize_email(uform.cleaned_data['email'])
            djangouser = User.objects.create_user(uform.cleaned_data['username'],
                                     email,
                                     uform.cleaned_data['password'])
            
            logger.debug("User created in database as " + djangouser.username)
            
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

            logger.debug("Signup request processed with the following info:" +
                            "\n\t Username: " + djangouser.username +
                            "\n\t Email: " + djangouser.email +
                            "\n\t First Name: " + djangouser.first_name +
                            "\n\t Last Name: " + djangouser.last_name +
                            "\n\t Date of Birth: " + str(djangouser._dateofbirth) +
                            "\n\t Gender: " + djangouser._gender +
                            "\n\t Height: " + str(djangouser._height) +
                            "\n\t Weight: " + str(djangouser._weight) +
                            "\n\t Notes: " + djangouser._notes
                        )
            logger.debug("Sending 'user_initiated' signal...")
            signals.user_initiated.send(sender=None, instance=djangouser,
                                dateofbirth=djangouser._dateofbirth,
                                gender=djangouser._gender,
                                height=djangouser._height,
                                weight=djangouser._weight,
                                notes=djangouser._notes)
            
            djangouser.save()
            logger.debug("User creation successful.")
            return HttpResponseRedirect('..')
    else:
        logger.info("Loading signup page...")
        uform = UserForm(instance=User())
        pform = UserprofileForm(instance=Userprofile())
    return render(request,
                  'healthtracker/signup.html',
                  {'user_form':uform, 'userprofile_form':pform}
                  )


@login_required
def profile(request):
    logger.info("Loading profile page...")
    return render(request, 'healthtracker/profile.html')


@login_required
def searchmeal(request):
    if request.method == "POST":
        logger.info("Food query results returned.")
        searchterm = request.POST.get('food')
        wrapper = ApiWrapper()
        results = wrapper.searchFood(searchterm)
        request.results = results
        return render(request, 'healthtracker/searchmeal.html')
    else:
        logger.info("Search food page accessed.")
        return render(request, 'healthtracker/searchmeal.html')
#    return HttpResponseRedirect('/healthtracker/profile')

@login_required
def fooddetails(request, ndbno):
    if request.method == "POST":
        unit = request.POST.get('unit')
        quantity = request.POST.get('quantity')
        ndbno = ndbno
        logger.info("Added " + str(quantity) + " " + str(unit) + "(s) of " + ndbno )
        request.notification = 'Added {} {}(s) of {}.'.format(quantity,unit,ndbno)
        return render(request, 'healthtracker/profile.html')
    else:
        request.ndbno = ndbno
        logger.info("Food details for " + ndbno)
        wrapper = ApiWrapper()
        report = wrapper.getFoodReport(ndbno)
        request.report = report
        measures = report["nutrients"][0]["measures"]
        request.measures = measures
        return render(request, 'healthtracker/fooddetails.html')
        

@login_required
def searchexercise(request):
    logger.info("Querying exercise...")
    return render(request, 'healthtracker/searchexercise.html')


@login_required
def addmeal(request):
    logger.info("Adding meal...")
    return render(request, 'healthtracker/addmeal.html')


@login_required
def addexercise(request):
    logger.info("Adding exercise...")
    return render(request, 'healthtracker/addexercise.html')


@login_required
def editprofile(request):
    logger.info("Loading edit profile page...")
    return render(request, 'healthtracker/editprofile.html')


def forgottenpassword(request):
    logger.info("Loading forgotten password...")
    return render(request, 'healthtracker/forgottenpassword.html')


def recoverpassword(request):
    logger.info("Recovering password...")
    return redirect('/healthtracker')
