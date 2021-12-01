from django.urls import path
from . import views

urlpatterns = [
    path('', views.wishlist, name='wishlist'),
    path('add/<uuid:sku>', views.add_to_wishlist, name='add_to_wishlist'),
    path('delete/<uuid:wishlist_id>',
         views.delete_from_wishlist,
         name='delete_from_wishlist'),
]
