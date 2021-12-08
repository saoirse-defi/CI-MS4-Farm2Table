from django import forms
from .widgets import ProductClearableFileUnit

from .models import Product, Category


class ProductForm(forms.ModelForm):
    """ Form for store owners to create product listings. """
    class Meta:
        model = Product
        exclude = ('seller_store',
                   'rating',
                   'sku',
                   'image_url',
                   'has_sizes',
                   'organic')

    image = forms.ImageField(label='Image', required=False,
                             widget=ProductClearableFileUnit)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'price': 'Price per 250g',
            'name': 'Product Name',
            'description': 'Write a short description of your product...',
        }

        self.fields['name'].widget.attrs['autofocus'] = True

        for field in self.fields:
            if field == 'price':
                placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            if field == 'name':
                placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            if field == 'description':
                placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False

        categories = Category.objects.all()
        cat_choices = [(c.category_id,
                        c.name) for c in categories]

        self.fields['category'].choices = cat_choices
