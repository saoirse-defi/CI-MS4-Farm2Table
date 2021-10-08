from django import forms
from django.forms.widgets import Select
from django.contrib.auth import get_user_model
from products.widgets import CustomClearableFileUnit

from .models import Store
from localflavor.ie.forms import IECountySelect, EircodeField, IE_COUNTY_CHOICES


User = get_user_model()


class StoreRegisterForm(forms.ModelForm):
    email = forms.EmailField(label='Email address')
    name = forms.CharField(label='Store Name')
    phone_number = forms.CharField(label='Phone')
    street_address1 = forms.CharField()
    street_address2 = forms.CharField()

    class Meta:
        model = Store
        fields = [
            'email',
            'name',
            'phone_number',
            'street_address1',
            'street_address2',

        ]

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        name = self.cleaned_data.get('name')
        #if password != password2:
            #raise forms.ValidationError("Passwords do not match!")
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError(
                "This email has already been registered to a different store.")
        return super(StoreRegisterForm, self).clean(*args, **kwargs)
