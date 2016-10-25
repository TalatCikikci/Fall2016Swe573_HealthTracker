from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.
@python_2_unicode_compatible
class Userbasic(models.Model):
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=200)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.username


@python_2_unicode_compatible
class Userprofile(models.Model):
    userbasic = models.ForeignKey(Userbasic, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, unique=True)
    dateofbirth = models.DateTimeField()
    gender = models.CharField(max_length=1, choices=(('M', 'Male'),('F', 'Female')))
    height = models.IntegerField()
    weight = models.IntegerField()
#    avatar = models.ImageField
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return '%s %s %s %s' % (self.firstname, self.lastname, self.email, self.notes)
