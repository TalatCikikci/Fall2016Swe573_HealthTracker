from django.test import TestCase
from django.contrib.auth.models import User, BaseUserManager

import datetime

from .models import Userprofile

import healthtracker.signals as signals

class SignupTests(TestCase):

    def test_only_one_userprofile_data_submitted_during_signup(self):
        
        email = BaseUserManager.normalize_email("talat.cikikci@gmail.com")
        djangouser = User.objects.create_user("talatusername",
                                              email,
                                              "talatpassword")
        djangouser.last_name = "Cikikci"
        djangouser.first_name = "Talat"
        djangouser._dateofbirth = datetime.date.today()
        djangouser._gender = "M"
        djangouser._height = "182"
        djangouser._weight = "80"
        djangouser._notes = "User's notes."
        
        signals.user_initiated.send(sender=None, 
                            instance=djangouser,
                            dateofbirth=djangouser._dateofbirth,
                            gender=djangouser._gender,
                            height=djangouser._height,
                            weight=djangouser._weight,
                            notes=djangouser._notes)
        
        djangouser.save()
        
        created_user = User.objects.get(username="talatusername")
        user_entries = Userprofile.objects.filter(user_id=created_user.id)
        
        self.assertEquals(len(user_entries),1)


    def test_check_gender_correct_during_signup(self):
        
        email = BaseUserManager.normalize_email("talat.cikikci@gmail.com")
        djangouser = User.objects.create_user("talatusername",
                                              email,
                                              "talatpassword")
        djangouser.last_name = "Cikikci"
        djangouser.first_name = "Talat"
        djangouser._dateofbirth = datetime.date.today()
        djangouser._gender = "M"
        djangouser._height = "182"
        djangouser._weight = "80"
        djangouser._notes = "User's notes."
        
        signals.user_initiated.send(sender=None, 
                            instance=djangouser,
                            dateofbirth=djangouser._dateofbirth,
                            gender=djangouser._gender,
                            height=djangouser._height,
                            weight=djangouser._weight,
                            notes=djangouser._notes)
        
        djangouser.save()
        
        created_user = User.objects.get(username="talatusername")
        user_entry = Userprofile.objects.get(user_id=created_user.id)
        
        self.assertEquals(user_entry.gender,"M")


    def test_check_weight_correct_during_signup(self):
        
        email = BaseUserManager.normalize_email("talat.cikikci@gmail.com")
        djangouser = User.objects.create_user("talatusername",
                                              email,
                                              "talatpassword")
        djangouser.last_name = "Cikikci"
        djangouser.first_name = "Talat"
        djangouser._dateofbirth = datetime.date.today()
        djangouser._gender = "M"
        djangouser._height = "182"
        djangouser._weight = "80"
        djangouser._notes = "User's notes."
        
        signals.user_initiated.send(sender=None, 
                            instance=djangouser,
                            dateofbirth=djangouser._dateofbirth,
                            gender=djangouser._gender,
                            height=djangouser._height,
                            weight=djangouser._weight,
                            notes=djangouser._notes)
        
        djangouser.save()
        
        created_user = User.objects.get(username="talatusername")
        user_entry = Userprofile.objects.get(user_id=created_user.id)
        
        self.assertEquals(user_entry.weight,80)


    def test_check_height_correct_during_signup(self):
        
        email = BaseUserManager.normalize_email("talat.cikikci@gmail.com")
        djangouser = User.objects.create_user("talatusername",
                                              email,
                                              "talatpassword")
        djangouser.last_name = "Cikikci"
        djangouser.first_name = "Talat"
        djangouser._dateofbirth = datetime.date.today()
        djangouser._gender = "M"
        djangouser._height = "182"
        djangouser._weight = "80"
        djangouser._notes = "User's notes."
        
        signals.user_initiated.send(sender=None, 
                            instance=djangouser,
                            dateofbirth=djangouser._dateofbirth,
                            gender=djangouser._gender,
                            height=djangouser._height,
                            weight=djangouser._weight,
                            notes=djangouser._notes)
        
        djangouser.save()
        
        created_user = User.objects.get(username="talatusername")
        user_entry = Userprofile.objects.get(user_id=created_user.id)
        
        self.assertEquals(user_entry.height,182)


    def test_check_notes_correct_during_signup(self):
        
        email = BaseUserManager.normalize_email("talat.cikikci@gmail.com")
        djangouser = User.objects.create_user("talatusername",
                                              email,
                                              "talatpassword")
        djangouser.last_name = "Cikikci"
        djangouser.first_name = "Talat"
        djangouser._dateofbirth = datetime.date.today()
        djangouser._gender = "M"
        djangouser._height = "182"
        djangouser._weight = "80"
        djangouser._notes = "User's notes."
        
        signals.user_initiated.send(sender=None, 
                            instance=djangouser,
                            dateofbirth=djangouser._dateofbirth,
                            gender=djangouser._gender,
                            height=djangouser._height,
                            weight=djangouser._weight,
                            notes=djangouser._notes)
        
        djangouser.save()
        
        created_user = User.objects.get(username="talatusername")
        user_entry = Userprofile.objects.get(user_id=created_user.id)
        
        self.assertEquals(user_entry.notes,"User's notes.")


    def test_check_birthday_correct_during_signup(self):
        
        email = BaseUserManager.normalize_email("talat.cikikci@gmail.com")
        djangouser = User.objects.create_user("talatusername",
                                              email,
                                              "talatpassword")
        djangouser.last_name = "Cikikci"
        djangouser.first_name = "Talat"
        djangouser._dateofbirth = datetime.date.today()
        djangouser._gender = "M"
        djangouser._height = "182"
        djangouser._weight = "80"
        djangouser._notes = "User's notes."
        
        signals.user_initiated.send(sender=None, 
                            instance=djangouser,
                            dateofbirth=djangouser._dateofbirth,
                            gender=djangouser._gender,
                            height=djangouser._height,
                            weight=djangouser._weight,
                            notes=djangouser._notes)
        
        djangouser.save()
        
        created_user = User.objects.get(username="talatusername")
        user_entry = Userprofile.objects.get(user_id=created_user.id)
        
        self.assertEquals(user_entry.dateofbirth,datetime.date.today())


    def test_check_password_is_not_plaintext(self):
        
        email = BaseUserManager.normalize_email("talat.cikikci@gmail.com")
        djangouser = User.objects.create_user("talatusername",
                                              email,
                                              "talatpassword")
        djangouser.last_name = "Cikikci"
        djangouser.first_name = "Talat"
        djangouser._dateofbirth = datetime.date.today()
        djangouser._gender = "M"
        djangouser._height = "182"
        djangouser._weight = "80"
        djangouser._notes = "User's notes."
        
        signals.user_initiated.send(sender=None, 
                            instance=djangouser,
                            dateofbirth=djangouser._dateofbirth,
                            gender=djangouser._gender,
                            height=djangouser._height,
                            weight=djangouser._weight,
                            notes=djangouser._notes)
        
        djangouser.save()
        
        created_user = User.objects.get(username="talatusername")
        
        self.assertNotEquals(created_user.password,"talatpassword")
