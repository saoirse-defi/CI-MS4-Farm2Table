from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q

from .filters import StoreFilter
from .forms import StoreRegisterForm, StoreUpdateForm
from profile.models import UserProfile
from .models import Store, County
from checkout.models import Order
from products.models import Product

# Create your views here.


def all_stores(request):
    """ A view to handle all products """

    stores = Store.objects.all()

    context = {
        'stores': stores,
    }

    return render(request, 'store/all_stores.html', context)


@login_required
def create_store(request):
    """ Allows user to create sales organisation. """
    current_user = UserProfile.objects.get(user=request.user)

    try:
        store = Store.objects.get(user=current_user)
    except Exception as e:
        store = None

    if request.method == 'POST':
        form = StoreRegisterForm(request.POST, request.FILES)
        if store is not None:
            messages.error(request,
                           'Organisation creation failed, '
                           'you can only have 1 store linked '
                           'to each account.')
            return redirect(reverse('view_store',
                                    args=[store.store_id, ]))
        else:
            if form.is_valid():
                store = form.save(commit=False)
                store.user = current_user
                store.save()
                messages.success(request, 'Store Organisation Created!')
                return redirect(reverse('view_store', args=[store.store_id, ]))
            else:
                messages.error(request, 'Organisation creation failed, '
                               'please check form details.')
    else:
        form = StoreRegisterForm()

    template = "store/create_store.html"
    context = {
        'form': form,
    }
    return render(request, template, context)


def my_store(request):
    try:
        current_user = UserProfile.objects.get(user=request.user)
    except Exception as e:
        current_user = None
        print(e)

    if current_user is not None:
        try:
            store = Store.objects.get(user=current_user)
        except Exception as e:
            store = None
            print(e)

        if store is not None:
            #form = StoreUpdateForm(instance=store)
            template = 'store/store.html'
            context = {
                'store': store,
                'current_user': current_user,
                #'form': form,
            }
            return render(request, template, context)
        else:
            messages.error(request, "No current store available, "
                           "if you wish to create one please do so below.")
            return redirect('view_profile')
    else:
        messages.error(request, "No current store available, "
                           "if you wish to create one please do so below.")
        return redirect('view_profile')


def view_store(request, store_id):
    try:
        current_user = UserProfile.objects.get(user=request.user)
    except Exception as e:
        current_user = None
        print(e)

    store = get_object_or_404(Store, pk=store_id)
    store_orders = Order.objects.all().filter(seller_store=store)
    store_products = Product.objects.all().filter(seller_store=store)

    form = StoreUpdateForm(instance=store)

    if store.user == current_user:
        template = 'store/store.html'
        context = {
            'store': store,
            'store_orders': store_orders,
            'store_products': store_products,
            'form': form,
            'current_user': current_user,
        }
        return render(request, template, context)
    else:
        template = 'store/store_customer.html'
        context = {
            'store': store,
            'store_orders': store_orders,
            'store_products': store_products,
            'current_user': current_user,
        }
        return render(request, template, context)


def edit_store(request, store_id):
    try:
        current_user = UserProfile.objects.get(user=request.user)
    except Exception as e:
        current_user = None
        print(e)

    store = get_object_or_404(Store, pk=store_id)

    if request.method == 'POST':
        form = StoreUpdateForm(request.POST, instance=store)
        if store.user == current_user:
            if form.is_valid():
                form.save()
                messages.success(request, "Seller profile updated successfully.")
                return redirect(reverse('view_store', args=[store.store_id, ]))
            else:
                messages.error(request, 'Please review store\'s details as '
                               'there appears to be an error.')
    else:
        form = StoreRegisterForm(instance=store)

    template = 'store/store.html'
    context = {
        'form': form,
        'store': store,
    }
    return render(request, template, context)


def delete_store(request, store_id):
    try:
        current_user = UserProfile.objects.get(user=request.user)
    except Exception as e:
        current_user = None
        print(e)

    store = get_object_or_404(Store, pk=store_id)

    if store.user == current_user:
        store.delete()
        messages.success(request, f'{store.name} has been deleted successfully.')
        return redirect(reverse('view_profile'))
    else:
        messages.error(request, 'You do not have the authority for this action')
        return redirect(reverse('view_store', args=[store.store_id, ]))


def local_producers(request):
    try:
        current_user = UserProfile.objects.get(user=request.user)
    except Exception as e:
        current_user = None
        print(e)

    if current_user is None:
        template = 'store/all_stores.html'
        context = {
            'current_user': current_user,
        }
        return render(request, template, context)
    else:
        if current_user.default_county is None:
            template = 'store/unknown_local_producers.html'
            context = {
                'current_user': current_user,
            }
            return render(request, template, context)

        else:
            local_stores = Store.objects.all().filter(
                           county=current_user.default_county)

            template = 'store/local_producers.html'
            context = {
                'current_user': current_user,
                'local_stores': local_stores,
            }
            return render(request, template, context)


def store_search(request):
    all_stores_list = Store.objects.all()
    counties = County.objects.all()
    query = None

    if request.GET.get('#store_search_form'):
        if 'county' in request.GET:
            query = request.GET['county']
            result = Store.objects.filter(Q(name__icontains=query))

    template = 'store/all_stores.html'

    context = {
        'all_stores_list': all_stores_list,
        'search_term': query,
        'counties': counties,
        'result': result,
    }

    return render(request, template, context)
