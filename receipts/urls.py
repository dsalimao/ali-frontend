from django.urls import path, re_path
from .onstart import on_startup
from . import views

app_name = 'receipts'

urlpatterns = [
    # ex: /receipts/pickup/
    path('pickup', views.pickup, name='pickup'),
    # ex: /receipts/pickup/endpoint/
    path('pickup/endpoint', views.pickup_endpoint, name='pickup_endpoint'),
    # ex: /receipts/5/
    path('<int:receipts_id>/', views.detail, name='detail'),
    # ex: /receipts/5/raw/
    path('<int:receipts_id>/results/', views.raw, name='raw'),
    # ex: /receipts/
    re_path(r'^', views.index, name='index'),
]

on_startup()