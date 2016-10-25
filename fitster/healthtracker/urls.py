from django.conf.urls import url

from . import views

app_name = 'healthtracker'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^registeruser/$', views.registeruser, name='registeruser'),
    url(r'^forgottenpassword/$', views.forgottenpassword, name='forgottenpassword'),
    url(r'^recoverpassword/$', views.recoverpassword, name='recoverpassword')
]
