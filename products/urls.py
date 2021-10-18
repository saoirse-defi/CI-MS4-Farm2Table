import uuid
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.all_products, name='products'),
    path('<uuid:product_id>/', views.product_detail, name='product_detail'),
    path('add/', views.add_product, name='add_product'),
    path('edit/<uuid:product_id>/', views.edit_product, name='edit_product'),
    path('delete/<uuid:product_id>/', views.delete_product, name='delete_product'),
    path('seller-product-management/', views.seller_product_management, name='seller_product_management'),
]