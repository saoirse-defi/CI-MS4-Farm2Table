from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import StoreRegisterForm

# Create your views here.


@login_required
def create_store(request):
    if request.method == 'POST':
        form = StoreRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            store = form.save()
            messages.success(request, 'Store Organisation Created!')
            return redirect(reverse('store', args=[store.id]))
        else:
            messages.error(request, 'Organisation creation failed, please check form details.')
    else:
        form = StoreRegisterForm()

    template = "store/create_store.html"
    context = {
        'form': form,
    }
    return render(request, template, context)
