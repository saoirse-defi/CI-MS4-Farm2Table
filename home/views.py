from django.shortcuts import render, reverse, redirect

from store.models import Store, County
from store.filters import StoreFilter

# Create your views here.


def index(request):
    """ A view to return to the index page """
    stores = Store.objects.all()

    county_store_filter = StoreFilter(request.GET, queryset=stores)
    stores = county_store_filter.qs 

    template = 'home/index.html'

    context = {
        'county_store_filter': county_store_filter,
        'stores': stores,

    }

    return render(request, template, context)
