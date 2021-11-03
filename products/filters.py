import django_filters

from .models import Product


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['sku', 'seller_store',
                   'name', 'description',
                   'price', 'has_sizes',
                   'organic', 'rating',
                   'image_url', 'image']
