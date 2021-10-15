from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages

from .forms import WishlistForm
from .models import Wishlist
from profile.models import UserProfile
from products.models import Product

# Create your views here.


def wishlist(request):

    profile = get_object_or_404(UserProfile, user=request.user)
    wishlist_all = Wishlist.objects.all()
    my_wishlist = []

    for wishlist_item in wishlist_all:
        if wishlist_item.user == profile:
            my_wishlist.append(wishlist_item)

    template = "wishlist/wishlist.html"
    context = {
        'my_wishlist': my_wishlist,
        'wishlist_all': wishlist_all,
    }
    
    return render(request, template, context)


def add_to_wishlist(request, sku):
    profile = get_object_or_404(UserProfile, user=request.user)

    product = get_object_or_404(Product, pk=sku)

    Wishlist.objects.update_or_create(
        user=profile, product=product
    )

    return redirect(reverse('wishlist'))
