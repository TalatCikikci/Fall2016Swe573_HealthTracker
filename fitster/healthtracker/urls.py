from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

app_name = 'healthtracker'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^forgottenpassword/$', views.forgottenpassword, name='forgottenpassword'),
    url(r'^recoverpassword/$', views.recoverpassword, name='recoverpassword')
]
