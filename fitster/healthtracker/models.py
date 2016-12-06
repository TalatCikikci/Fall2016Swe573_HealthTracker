from django.db import models
from django import forms
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import user_logged_in

from .utils import UserUtils
import healthtracker.signals as signals

# Create your models here.

@python_2_unicode_compatible
class Userprofile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE, 
                                related_name="userprofile")
    dateofbirth = models.DateField()
    gender = models.CharField(max_length=1, choices=(
                                                    ('M', 'Male'),
                                                    ('F', 'Female')))
    height = models.PositiveIntegerField()
    weight = models.PositiveIntegerField()
    notes = models.TextField(blank=True, null=True)


@receiver(signals.user_initiated, dispatch_uid="user_initiator")
def create_user_profile(instance, dateofbirth, gender, height, weight, notes, **kwargs):
        Userprofile.objects.create(user=instance,
                                   dateofbirth = dateofbirth,
                                   gender = gender,
                                   height = height,
                                   weight = weight,
                                   notes = notes)
                                   

@receiver(user_logged_in, dispatch_uid="bmi_calculator")
def calculate_bmi(sender, request, user, **kwargs):
    util = UserUtils(user)
    
    request.session['bmi'] = util.getBmi()
