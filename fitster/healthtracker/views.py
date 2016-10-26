from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext

from .models import Userbasic, Userprofile
from .forms import UserbasicForm, UserprofileForm

# Create your views here.
def index(request):
    return render(request,
                  'healthtracker/login.html'
                  )

def login(request):
    return render(request,
                  'healthtracker/profile.html'
                  )

def signup(request):
    if request.method == "POST":
        bform = UserbasicForm(request.POST, instance=Userbasic())
        pform = UserprofileForm(request.POST, instance=Userprofile())
        if bform.is_valid() and pform.is_valid():
            new_user = bform.save()
            new_profile = pform.save(commit=False)
            new_profile.userbasic = new_user
            new_profile.save()
            return HttpResponseRedirect('..')
    else:
        bform = UserbasicForm(instance=Userbasic())
        pform = UserprofileForm(instance=Userprofile())
    return render(request,
                  'healthtracker/signup.html',
                  {'userbasic_form':bform, 'userprofile_form':pform}
                  )

def forgottenpassword(request):
    return render(request, 'healthtracker/forgottenpassword.html')

def recoverpassword(request):
    return render(request, 'healthtracker/login.html')
