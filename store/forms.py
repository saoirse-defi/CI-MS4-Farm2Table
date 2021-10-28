from django import forms
from django.forms.widgets import Select
from django.contrib.auth import get_user_model
from products.widgets import CustomClearableFileUnit
from django_iban.fields import IBANField

from .models import Store, County
from localflavor.ie.forms import EircodeField


User = get_user_model()


class StoreRegisterForm(forms.ModelForm):
    class Meta:
        model = Store
        exclude = ('user', 'rating', 'organic', 'street_address2')

    image = forms.ImageField(label='Image', required=False,
                             widget=CustomClearableFileUnit)

    email = forms.EmailField(label='Email address')
    name = forms.CharField(label='Store Name')
    phone_number = forms.CharField(label='Phone')
    iban = IBANField()
    street_address1 = forms.CharField()
    town = forms.CharField()
    county = forms.ModelChoiceField(queryset=County.objects.all(), initial=0)
    postcode = EircodeField()

    def clean(self, *args, **kwargs):
        counties = County.objects.all()
        friendly_counties = [(c.id, c.get_friendly_name()) for c in counties]
        self.fields['county'].choices = friendly_counties

        email = self.cleaned_data.get('email')
        email_qs = User.objects.filter(email=email)

        if email_qs.exists():
            raise forms.ValidationError(
                "This email has already been registered to a different store.")

        return super(StoreRegisterForm, self).clean(*args, **kwargs)
