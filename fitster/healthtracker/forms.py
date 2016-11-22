from django.forms import ModelForm
from django.conf import settings
from django.contrib.auth.models import User

from .models import Userprofile

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username',
                  'password',
                  'first_name',
                  'last_name',
                  'email'
                  ]

class UserprofileForm(ModelForm):
    class Meta:
        model = Userprofile
        fields = ['dateofbirth',
                  'gender',
                  'height',
                  'weight',
                  'notes'
                  ]
