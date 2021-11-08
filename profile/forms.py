from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import (
    authenticate,
    get_user_model
)

from .models import UserProfile
from store.models import County
from localflavor.ie.forms import EircodeField


User = get_user_model()


class UserLoginForm(forms.ModelForm):
    email = forms.EmailField(label='Email address')
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'email',
            'password',
        ]

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        user = User.objects.get(email=email)

        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError({"email":
                                         "This email is not registered"})
        if not user.check_password(password):
            raise forms.ValidationError({"password":
                                         "Incorrect password"})
        
        return self.cleaned_data

        #user = authenticate(email=email, password=password)
        #if not user:
        #    raise forms.ValidationError('This user does not exist')
        #if not user.check_password(password):
        #    raise forms.ValidationError('Incorrect password')
        #if not user.is_active:
         #   raise forms.ValidationError('This user is not active')
        #return self.cleaned_data


class UserRegisterForm(forms.ModelForm):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
        ]

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError({"username":
                                         "This username has "
                                         "already been registered"})
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError({"email":
                                         "This email has "
                                         "already been registered"})
        if len(password) < 5:
            raise forms.ValidationError({"password":
                                         "Please use a password "
                                         "with more than 4 characters"})
        return self.cleaned_data


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)

    # county = forms.ModelChoiceField(queryset=County.objects.all(), initial=0)

    def __init__(self, *args, **kwargs):
        """Adds placeholders and classes,
            remove auto-gen labels and sets
            autofocus on first field."""

        super().__init__(*args, **kwargs)
        #placeholders = {
         #   'default_phone_number': 'Phone',
          #  'default_street_address1': 'Street Address Line 1',
           # 'default_street_address2': 'Street Address Line 2',
            #'default_town': 'Town/City',
            #'default_postcode': 'Eircode',
        #}

        self.fields['default_phone_number'].widget.attrs['autofocus'] = True

        #for field in self.fields:
            #if field != 'default_country':
                #if self.fields[field].required:
                    #placeholder = f'{placeholders[field]} *'
                #else:
                    #placeholder = placeholders[field]
            #self.fields[field].widget.attrs['placeholder'] = placeholder
        #self.fields[field].widget.attrs['class'] = 'border-black rounded-0 profile-form-input'
        #self.fields[field].label = False
        self.fields['default_county'] = forms.ModelChoiceField(
                                        queryset=County.objects.all(),
                                        initial=0)
        self.fields['default_postcode'] = EircodeField()
