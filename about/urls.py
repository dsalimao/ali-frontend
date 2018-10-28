import os
from django.urls import path
from . import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()
app_name = 'about'

urlpatterns = [
    path('ali', views.about_ali, name='about_ali'),
    path('me', views.about_me, name='about_me'),
]