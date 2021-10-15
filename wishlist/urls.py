from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.wishlist, name='wishlist'),
    path('add/<uuid:sku>', views.add_to_wishlist, name='add_to_wishlist'),
]