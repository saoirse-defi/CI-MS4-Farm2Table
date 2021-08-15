from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.view_bag, name='view_bag')
]
