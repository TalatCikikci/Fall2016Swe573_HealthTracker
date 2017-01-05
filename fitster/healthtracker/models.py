from django.db import models
from django import forms
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import user_logged_in

from .utils import UserUtils
import healthtracker.signals as signals


# Userprfile model is where all personal information of the user is kept.
@python_2_unicode_compatible
class Userprofile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE, 
                                related_name="userprofile")
    dateofbirth = models.DateField()
    gender = models.CharField(max_length=1, 
                              choices=(('M', 'Male'),
                                       ('F', 'Female')))
    height = models.PositiveIntegerField(help_text='Measured in (cm)')
    weight = models.PositiveIntegerField(help_text='Measured in (kg)')
    notes = models.TextField(blank=True, 
                             null=True)


# Userhistory model keeps track of any food or activity the user has saved.
class Userhistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    item_no = models.IntegerField()
    item_name = models.CharField(max_length=200)
    item_quantity = models.IntegerField()
    item_unit = models.CharField(max_length=50)
    item_unit_modifier = models.DecimalField(max_digits=6, 
                                             decimal_places=1)
    item_date = models.DateField()


# Userrecipe holds any recipes created by users and relates them.
class Userrecipe(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    recipe_name = models.CharField(max_length=100)


# Recipeitems keeps the ingredients of a recipe and relates them.
class Recipeitems(models.Model):
    recipe = models.ForeignKey(Userrecipe,
                               on_delete=models.CASCADE)
    item_ndbno = models.IntegerField()
    item_quantity = models.IntegerField()


# Itemcalories keeps the calorie values of history items.
class Itemcalories(models.Model):
    history_item = models.ForeignKey(Userhistory,
                                     on_delete=models.CASCADE)
    item_calories = models.DecimalField(max_digits=6, 
                                        decimal_places=1)


# Recipeitems keeps the nutrient values of history items.
class Itemnutrients(models.Model):
    history_item = models.ForeignKey(Userhistory,
                                     on_delete=models.CASCADE)
    item_nutrientdict = models.IntegerField()


# Following are the signal reciever implementations.

# create_user_profile method creates a Userprofile object and fills in the 
# related database tables when a new user is created.
@receiver(signals.user_initiated, dispatch_uid="user_initiator")
def create_user_profile(instance, dateofbirth, gender, height, weight, notes, **kwargs):
        Userprofile.objects.create(user=instance,
                                   dateofbirth = dateofbirth,
                                   gender = gender,
                                   height = height,
                                   weight = weight,
                                   notes = notes)
                                   

# calculate_bmi method calculates the BMI value of the user when the user logs
# into the system.
@receiver(user_logged_in, dispatch_uid="bmi_calculator")
def calculate_bmi(sender, request, user, **kwargs):
    util = UserUtils(user)
    request.session['bmi'] = util.getBmi()

# record_history method creates a Userhistory object and fills in the 
# related database tables when a user saves an activity or food.
@receiver(signals.item_add_requested, dispatch_uid="item_logger")
def record_history(itemno, itemname, itemquantity, itemunit, itemmodifier, itemdate, userid, **kwargs):
    history_item = Userhistory.objects.create(item_no = itemno,
                                              item_name = itemname,
                                              item_quantity=itemquantity,
                                              item_unit=itemunit,
                                              item_unit_modifier=itemmodifier,
                                              item_date=itemdate,
                                              user_id=userid)
    return history_item

# record_calories method created an Itemcalories object and fills in the 
# related database tables when an item is successfully logged to the database.
@receiver(signals.item_added, dispatch_uid="item_calorie_adder")
def record_calories(historyitem, itemcalories, itemquantity, itemmodifier, **kwargs):
    itemcalories = (itemcalories/100)*itemmodifier*itemquantity
    Itemcalories.objects.create(history_item = historyitem,
                                item_calories = itemcalories)
