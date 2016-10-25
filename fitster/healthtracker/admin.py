from django.contrib import admin

# Register your models here.
from .models import Userbasic, Userprofile

admin.site.register(Userbasic)
admin.site.register(Userprofile)
