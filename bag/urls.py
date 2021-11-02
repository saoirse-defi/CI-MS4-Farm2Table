from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_bag, name='view_bag'),
    path('add/<product_id>/', views.add_to_bag, name='add_to_bag'),
    path('adjust/<product_id>/', views.adjust_bag, name='adjust_bag'),
    path('remove/<product_id>/',
         views.remove_from_bag, name='remove_from_bag'),
]
