import os
from django.urls import path, re_path
from . import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()
app_name = 'oauth'

urlpatterns = [
    path('start_oauth_flow', views.start_oauth_flow, name='start_oauth_flow'),
    re_path(r'^oauth_return', views.oauth_return, name='oauth_return'),
]