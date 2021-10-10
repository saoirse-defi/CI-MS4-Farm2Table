from django.shortcuts import render

# Create your views here.


def wishlist(request):

    wishlist_all = Wishlist.objects.all()
    my_wishlist = []

    for wishlist_item in wishlist_all:
        if wishlist_item.user == request.user:
            my_wishlist.append(wishlist_item)

    template = "wishlist/wishlist.html"
    context = {
        'my_wishlist': my_wishlist,
    }
    return render(request, template, context)