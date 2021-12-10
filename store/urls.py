from django.urls import path
from . import views

urlpatterns = [
    path('all_stores/', views.all_stores, name='all_stores'),
    path('search/', views.store_search, name='store_search'),
    path('create_store/', views.create_store, name='create_store'),
    path('<uuid:store_id>/', views.view_store, name='view_store'),
    path('my_store/', views.my_store, name='my_store'),
    path('edit_store/<uuid:store_id>/', views.edit_store, name='edit_store'),
    path('delete_store/<uuid:store_id>/',
         views.delete_store, name='delete_store'),
    path('local_producers/', views.local_producers, name='local_producers'),
]
