from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages

from .models import Wishlist
from profile.models import UserProfile
from products.models import Product

# Create your views here


def wishlist(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    my_wishlist = Wishlist.objects.all().filter(user=profile)

    template = "wishlist/wishlist.html"
    context = {
        'my_wishlist': my_wishlist,
    }

    return render(request, template, context)


def add_to_wishlist(request, sku):

    profile = get_object_or_404(UserProfile, user=request.user)

    product = get_object_or_404(Product, pk=sku)

    Wishlist.objects.update_or_create(
        user=profile, product=product
    )

    messages.add_message(request, 50, 'Item added to your wishlist.')

    return redirect(reverse('product_detail', args=[product.sku]))


def delete_from_wishlist(request, wishlist_id):
    wishlist_item = get_object_or_404(Wishlist, pk=wishlist_id)

    wishlist_item.delete()

    messages.add_message(request, 50, 'Item removed from your wishlist.')

    return redirect(reverse('product_detail',
                            args=[wishlist_item.product.sku]))
