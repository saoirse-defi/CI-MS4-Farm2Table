from django.shortcuts import render, reverse, redirect

from store.models import Store, County
from store.views import store_search

# Create your views here.


def index(request):
    """ A view to return to the index page """
    counties = County.objects.all()
    

    template = 'home/index.html'

    context = {
        'counties': counties,

    }

    return render(request, template, context)
