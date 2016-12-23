from django.forms import ModelForm, PasswordInput, TextInput, EmailInput, DateInput, Select, NumberInput, Textarea, SelectDateWidget, ValidationError, CharField
from django.conf import settings
from django.contrib.auth.models import User

import datetime

from .models import Userprofile

class UserForm(ModelForm):
    
    password = CharField(widget=PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = CharField(widget=PasswordInput(attrs={'class': 'form-control'}))
    
    class Meta:
        
        model = User
        
        fields = ['username',
                  'password',
                  'confirm_password',
                  'first_name',
                  'last_name',
                  'email'
                  ]
        
        widgets = {
            'username': TextInput(attrs={'class': 'form-control'}),
            'password': PasswordInput(attrs={'masked': True, 'class': 'form-control'}),
            'confirm_password': PasswordInput(attrs={'masked': True, 'class': 'form-control'}),
            'first_name': TextInput(attrs={'class': 'form-control'}),
            'last_name': TextInput(attrs={'class': 'form-control'}),
            'email': EmailInput(attrs={'class': 'form-control'}),
        }
    
    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise ValidationError(
                "'Password' and 'Confirm Password' fields do not match!"
            )

class UserprofileForm(ModelForm):
    
    class Meta:
        
        year = datetime.datetime.now().year
        
        model = Userprofile
        
        fields = ['dateofbirth',
                  'gender',
                  'height',
                  'weight',
                  'notes'
                  ]
        
        widgets = {
            'dateofbirth': SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day"), years=range(1900, year+1), attrs={'class': 'form-control'}),
            'gender': Select(attrs={'masked': True, 'class': 'form-control'}),
            'height': NumberInput(attrs={'class': 'form-control'}),
            'weight': NumberInput(attrs={'class': 'form-control'}),
            'notes': Textarea(attrs={'class': 'form-control'}),
        }

class ChangepasswordForm(ModelForm):
    
    password = CharField(widget=PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = CharField(widget=PasswordInput(attrs={'class': 'form-control'}))
    
    class Meta:
        
        model = User
        
        fields = ['password',
                  'confirm_password',
                  ]
                  
        widgets = {
            'password': PasswordInput(attrs={'masked': True, 'class': 'form-control'}),
            'confirm_password': PasswordInput(attrs={'masked': True, 'class': 'form-control'})
            }
    
    def clean(self):
        cleaned_data = super(ChangepasswordForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise ValidationError(
                "'Password' and 'Confirm Password' fields do not match!"
            )
