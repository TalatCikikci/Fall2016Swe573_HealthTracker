from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User, BaseUserManager, AbstractBaseUser
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import logging, datetime

from .models import Userprofile, Userhistory, Userrecipe, Recipeitems
from .forms import UserForm, UserprofileForm
from .utils import UserUtils, ApiWrapper
import healthtracker.signals as signals

# Initialize the logger object
logger = logging.getLogger('django')


# Display the login page when user goes to the landing page.
def index(request):
    
    return render(request,
                  'healthtracker/login.html'
                  )


# Authenticates the user using the information ubmitted in the login field.
# If the user is authenticated then the user is logged into the profile page.
# If the user is not authenticated, then the user is redirected to the login page.
def login(request):
    
    username = request.POST.get('username')
    password = request.POST.get('password')
    logger.info("Login request as" +
                "\n\tUsername: " + 
                username)
    user = authenticate(username=username, password=password)
    
    if user is not None:
        # Using "login" here clashes with the view named "login" so
        # we use "auth_login" instead.
        auth_login(request, user)
        logger.info("User succesfully logged in as " + 
                    user.username)
        return redirect('/healthtracker/profile')
    
    else:
        logger.info("User authentication failed with given credentials!")
        return redirect('/healthtracker')


# User's session is destroyed and the user is redirected to the login page.
def logout(request):
    
    logger.info("Logging out...")
    # Using "logout" here clashes with the view named "logout" so 
    # we use "auth_logout" instead.
    auth_logout(request)
    logger.info("User " + 
                request.user.username + 
                " logged out.")
    return redirect('/healthtracker')


# User is redirected to the login page after user's account info is saved to the database
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
            
            logger.debug("User created in database as " + 
                         djangouser.username)
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
            signals.user_initiated.send(sender=None, 
                                instance=djangouser,
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


# Displays the profile template.
# login_required annotation prevents the users from vieweing this page without 
# creating a session. Users without session are redirected to the login page.
@login_required
def profile(request):
    
    uid = request.user.id
    logger.info("Loading profile page...")
    return render(request, 
                  'healthtracker/profile.html', 
                  {'recentfoodhistory':Userhistory.objects.filter(user_id=uid, 
                                                        item_no__gt=821, 
                                                        item_date=datetime.date.today()), 
                   'recentexercisehistory':Userhistory.objects.filter(user_id=uid, 
                                                        item_no__lte=821, 
                                                        item_date=datetime.date.today())}
                  )


# Quries the API for the submitted keyword. Displays the result as a list.
# Users can click the food name to go to food detail page.
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


# Queries the nutrient report of the food using the ndbno and displays the 
# list of nutrients contained. 
@login_required
def fooddetails(request, ndbno):
    
    if request.method == "POST":
        itemno = ndbno
        itemunit = request.POST.get('unit')
        itemquantity = request.POST.get('quantity')
        itemname = request.POST.get('itemname')
        itemdate = datetime.datetime.strptime(request.POST['date'], "%m/%d/%Y")
        signals.item_added.send(sender=None,
                            itemno=itemno,
                            itemname=itemname,
                            itemquantity=itemquantity,
                            itemunit=itemunit, 
                            itemdate=itemdate,
                            userid= request.user.id)
        logger.info("Added " + 
                    str(itemquantity) + 
                    " " + 
                    str(itemunit) + 
                    "(s) of " + 
                    itemname + 
                    " (ndbno = " 
                    + itemno + 
                    ").")
        request.notification = 'Added {} {}(s) of "{}".'.format(itemquantity,itemunit,itemname)
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


# Queries and returns a list of exercises.
@login_required
def searchexercise(request):
    
    if request.method == "POST":
        itemno_and_itemname = request.POST.get('exercise')
        itemno = itemno_and_itemname.split('_')[0]
        itemname = itemno_and_itemname.split('_')[1]
        itemunit = 'minutes'
        itemquantity = request.POST.get('duration')
        itemdate = datetime.datetime.strptime(request.POST['date'], "%m/%d/%Y")
        signals.item_added.send(sender=None,
                            itemno=itemno,
                            itemname=itemname,
                            itemquantity=itemquantity,
                            itemunit=itemunit, 
                            itemdate=itemdate,
                            userid= request.user.id)
        logger.info("Added " + 
                    str(itemquantity) + 
                    " " + 
                    str(itemunit) + 
                    "(s) of " + 
                    itemname + 
                    " (activity = " 
                    + itemno + 
                    ").")
        request.notification = 'Added {} {}(s) of "{}".'.format(itemquantity,itemunit,itemname)
        return render(request, 'healthtracker/profile.html')
    
    else:
        logger.info("Querying exercise...")
        wrapper = ApiWrapper()
        activities = wrapper.getActivities()
        activityGroups = wrapper.getActivityGroups()
        request.activities = activities
        request.activityGroups = activityGroups
        return render(request, 'healthtracker/searchexercise.html')


@login_required
def foodhistory(request):
    uid = request.user.id
    if request.method == "POST":
        search_date = request.POST.get('date')
        if search_date:
            query_date = datetime.datetime.strptime(search_date, "%m/%d/%Y")
            return render(request, 
                  'healthtracker/foodhistory.html', 
                  {'history':Userhistory.objects.filter(user_id=uid, 
                                                        item_no__gt=821,
                                                        item_date=query_date)}
            )
        else:
            return render(request, 
                  'healthtracker/foodhistory.html', 
                  {'history':Userhistory.objects.filter(user_id=uid, 
                                                        item_no__gt=821)}
            )
        
    else:
        return render(request, 
                  'healthtracker/foodhistory.html', 
                  {'history':Userhistory.objects.filter(user_id=uid, 
                                                        item_no__gt=821)}
                  )

@login_required
def exercisehistory(request):
    uid = request.user.id
    if request.method == "POST":
        search_date = request.POST.get('date')
        if search_date:
            query_date = datetime.datetime.strptime(search_date, "%m/%d/%Y")
            return render(request, 
                  'healthtracker/exercisehistory.html', 
                  {'history':Userhistory.objects.filter(user_id=uid, 
                                                        item_no__lte=821,
                                                        item_date=query_date)}
            )
        else:
            return render(request, 
                  'healthtracker/exercisehistory.html', 
                  {'history':Userhistory.objects.filter(user_id=uid, 
                                                        item_no__lte=821)}
            )
        
    else:
        return render(request, 
                  'healthtracker/exercisehistory.html', 
                  {'history':Userhistory.objects.filter(user_id=uid, 
                                                        item_no__lte=821)}
                  )

# Deprecated
@login_required
def addmeal(request):
    
    logger.info("Adding meal...")
    return render(request, 'healthtracker/addmeal.html')


# Deprecated
@login_required
def addexercise(request):
    
    logger.info("Adding exercise...")
    return render(request, 'healthtracker/addexercise.html')


# Displays and processes profile information to be edited.
@login_required
def editprofile(request):
    
    logger.info("Loading edit profile page...")
    return render(request, 'healthtracker/editprofile.html')


# Displays the forgotten password page.
def forgottenpassword(request):
    
    logger.info("Loading forgotten password...")
    return render(request, 'healthtracker/forgottenpassword.html')


# Processes the password rcovery request.
def recoverpassword(request):
    
    logger.info("Recovering password...")
    return redirect('/healthtracker')
