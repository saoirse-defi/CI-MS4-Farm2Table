import uuid
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('all_stores/', views.all_stores, name='all_stores'),
    path('search/', views.store_search, name='store_search'),
    path('create_store/', views.create_store, name='create_store'),
    path('<uuid:store_id>/', views.view_store, name='view_store'),
    path('edit_store/<uuid:store_id>/', views.edit_store, name='edit_store'),
    path('local_producers/', views.local_producers, name='local_producers'),
]
