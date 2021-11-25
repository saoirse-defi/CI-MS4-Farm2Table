from django import forms
from django.contrib.auth import get_user_model
from django_iban.fields import IBANField

from .widgets import StoreClearableFileUnit
from .models import Store, County
from localflavor.ie.forms import EircodeField
from django_countries.fields import CountryField


User = get_user_model()


class StoreRegisterForm(forms.ModelForm):
    class Meta:
        model = Store
        exclude = ('user', 'rating', 'organic', 'street_address2', 'image_url')

    image = forms.ImageField(label='Image', required=False,
                             widget=StoreClearableFileUnit)
    description = forms.CharField()
    email = forms.EmailField(label='Email address')
    name = forms.CharField(label='Store Name')
    phone_number = forms.CharField(label='Phone')
    iban = IBANField()
    street_address1 = forms.CharField()
    town = forms.CharField()
    county = forms.ModelChoiceField(queryset=County.objects.order_by('name'),
                                    initial=0)
    postcode = EircodeField()

    def clean(self, *args, **kwargs):
        counties = County.objects.order_by('name')
        friendly_counties = [(c.id, c.name) for c in counties]
        self.fields['county'].choices = friendly_counties

        return super(StoreRegisterForm, self).clean(*args, **kwargs)


class StoreUpdateForm(forms.ModelForm):
    """ Creates and validates Store update form."""
    class Meta:
        model = Store
        exclude = ('store_id', 'user', 'organic', 'rating', 'image_url')

    def __init__(self, *args, **kwargs):
        """Adds placeholders and classes,
            remove auto-gen labels and sets
            autofocus on first field."""

        super().__init__(*args, **kwargs)

        self.fields['county'] = forms.ModelChoiceField(queryset=County.objects.order_by('name'),
                                                       initial=0)
        self.fields['country'] = CountryField().formfield()
        self.fields['postcode'] = EircodeField()
