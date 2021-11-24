import django_filters

from .models import Store


class StoreFilter(django_filters.FilterSet):
    class Meta:
        model = Store
        fields = '__all__'
        exclude = ['store_id', 'user', 'name', 'description', 'email',
                   'phone_number', 'street_address1', 'street_address2',
                   'town', 'country', 'postcode', 'organic', 'iban',
                   'rating', 'image_url', 'image']
        order_by = 'name'
