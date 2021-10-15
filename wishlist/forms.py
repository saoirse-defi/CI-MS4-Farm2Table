from django import forms

from .models import Wishlist


class WishlistForm(forms.ModelForm):
    class Meta:
        model = Wishlist
        exclude = ('wishlist_id', 'user', 'product')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
