from django.forms import ModelForm, Form

from .models import Userbasic, Userprofile

class UserbasicForm(ModelForm):
    class Meta:
        model = Userbasic
        fields = ['username',
                  'password'
                  ]

class UserprofileForm(ModelForm):
    class Meta:
        model = Userprofile
        fields = ['firstname',
                  'lastname',
                  'email',
                  'dateofbirth',
                  'gender',
                  'height',
                  'weight',
                  'notes'
                  ]
