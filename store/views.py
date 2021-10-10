from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import StoreRegisterForm
from profile.models import UserProfile
from .models import Store

# Create your views here.


@login_required
def create_store(request):
    if request.method == 'POST':
        stores = Store.objects.all()
        form = StoreRegisterForm(request.POST)
        for _store in stores:
            if _store.user == request.user:
                messages.error(request, 'Organisation creation failed, you can only have 1 store linked to each account.')
                return redirect(reverse('view_store', args=[_store.store_id, ]))

        if form.is_valid():
            store = form.save(commit=False)
            store.user = request.user
            store.save()
            messages.success(request, 'Store Organisation Created!')
            return redirect(reverse('view_store', args=[_store.store_id, ]))
        else:
            messages.error(request, 'Organisation creation failed, please check form details.')
    else:
        form = StoreRegisterForm()

    template = "store/create_store.html"
    context = {
        'form': form,
    }
    return render(request, template, context)


def view_store(request, store_id):
    store = get_object_or_404(Store, pk=store_id)

    template = 'store/store.html'
    context = {
        'store': store,
    }
    return render(request, template, context)

