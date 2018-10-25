from django.urls import path, re_path
from .onstart import on_startup
from . import views

app_name = 'receipts'

urlpatterns = [
    # ex: /receipts/pickup/
    path('pickup', views.pickup, name='pickup'),
    # ex: /receipts/pickup/endpoint/
    path('pickup/endpoint', views.pickup_endpoint, name='pickup_endpoint'),
    # ex: /receipts/search
    path('search_receipts', views.search_receipts, name='search_receipts'),
    # ex: /receipts/get_detail/5/
    path('get_detail/<int:receipts_id>', views.get_detail, name='get_detail'),
    # ex: /receipts/get_raw/5
    path('get_raw/<int:receipts_id>', views.get_raw, name='get_raw'),
    # ex: /receipts/get_last_sync/ali
    path('get_last_sync/<str:receipts_id>', views.get_last_sync, name='get_last_sync'),
    # ex: /receipts/get_last_sync/ali
    path('update_last_sync', views.update_last_sync, name='update_last_sync'),
    # ex: /receipts/
    re_path(r'^', views.index, name='index'),
]

on_startup()