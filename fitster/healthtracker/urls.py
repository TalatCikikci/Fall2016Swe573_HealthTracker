from django.conf.urls import url

from . import views

app_name = 'healthtracker'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^searchmeal/$', views.searchmeal, name='searchmeal'),
    url(r'^searchexercise/$', views.searchexercise, name='searchexercise'),
    url(r'^fooddetails/(?P<ndbno>[0-9]+)/$', views.fooddetails, name='fooddetails'),
    url(r'^foodhistory/$', views.foodhistory, name='foodhistory'),
    url(r'^exercisehistory/$', views.exercisehistory, name='exercisehistory'),
    url(r'^addmeal/$', views.addmeal, name='addmeal'),
    url(r'^addexercise/$', views.addexercise, name='addexercise'),
    url(r'^editprofile/$', views.editprofile, name='editprofile'),
    url(r'^forgottenpassword/$', views.forgottenpassword, name='forgottenpassword'),
    url(r'^recoverpassword/$', views.recoverpassword, name='recoverpassword')
]
