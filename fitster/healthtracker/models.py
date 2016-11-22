from django.db import models
from django import forms
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
from django.dispatch import receiver
from django.db.models.signals import post_save

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


@receiver(post_save, sender=settings.AUTH_USER_MODEL, dispatch_uid="user_profile_creator")
def create_user_profile(sender, instance, created, **kwargs):
    if not created:
        Userprofile.objects.create(user=instance,
                                   dateofbirth = instance._dateofbirth,
                                   gender = instance._gender,
                                   height = instance._height,
                                   weight = instance._weight,
                                   notes = instance._notes)
