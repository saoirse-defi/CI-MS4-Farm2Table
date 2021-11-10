from django import forms
from django.contrib.auth import (
    get_user_model
)

from .models import UserProfile
from store.models import County
from localflavor.ie.forms import EircodeField


User = get_user_model()


class UserLoginForm(forms.ModelForm):
    """ Handles user login form validation."""
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

        try:
            user = User.objects.get(email=email)
        except Exception as e:
            user = None
        
        if user is None:
            raise forms.ValidationError({"email":
                                            "This email is not registered"})
        else:
            if not user.check_password(password):
                raise forms.ValidationError({"password":
                                            "Incorrect password"})
        return self.cleaned_data

        #if user is not None:
         #   if not User.objects.filter(email=email).exists():
          #      raise forms.ValidationError({"email":
           #                                 "This email is not registered"})
            #if not user.check_password(password):
             #   raise forms.ValidationError({"password":
              #                              "Incorrect password"})


class UserRegisterForm(forms.ModelForm):
    """ Handles user registration form validation."""
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
    """ Creates and validates UserProfile form."""
    class Meta:
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        """Adds placeholders and classes,
            remove auto-gen labels and sets
            autofocus on first field."""

        super().__init__(*args, **kwargs)

        # self.fields['default_phone_number'].widget.attrs['autofocus'] = True
        self.fields['default_county'] = forms.ModelChoiceField(
                                        queryset=County.objects.order_by('name'),
                                        initial=0)
        self.fields['default_postcode'] = EircodeField()
