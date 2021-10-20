from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from django.contrib.auth.decorators import login_required

from .models import Product, Category
from .forms import ProductForm
from profile.models import UserProfile
from store.models import Store

# Custom Decorators


def superuser_required(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.error(request, 'Sorry only store owners can do that.')
            return redirect(reverse('products'))
        else:
            return func(request)
    return wrapper


def store_required(func):  # not working properly
    def wrapper(request, *args, **kwargs):
        stores = Store.objects.all()
        for store in stores:
            if store.user == request.user:
                return func(request)
            else:
                messages.error(request,
                               "Only store owners can create & sell products.")
                return redirect(reverse('profile'))
    return wrapper


# Product Views

def all_products(request):
    """ A view to handle all products """

    products = Product.objects.all()

    context = {
        'products': products,
    }

    return render(request, 'products/products.html', context)


def product_search(request):
    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request,
                               ("You didn't enter any search criteria!"))
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    template = 'products/products.html'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, template, context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    store = get_object_or_404(Store, pk=product.seller_store.store_id)

    context = {
        'product': product,
        'store': store,
    }
    return render(request, 'products/product_detail.html', context)


# @store_required
@login_required
# @superuser_required
def add_product(request):
    """ Add a product to the store. """
    stores = Store.objects.all()
    users = UserProfile.objects.all()

    for user in users:
        if user.user == request.user:
            current_user = user

    for store in stores:
        if store.user == current_user:
            my_store = store
            if request.method == 'POST':
                form = ProductForm(request.POST, request.FILES)
                if form.is_valid():
                    product = form.save(commit=False)
                    product.seller_store = my_store
                    product.save()
                    messages.success(request, 'Successfully added product!')
                    return redirect(reverse(
                                    'product_detail', args=[product.sku, ]))
                else:
                    messages.error(request,
                                   'Failed to add product.'
                                   'Please ensure the form is valid.')
            else:
                form = ProductForm()
        else:
            messages.error(request, 'Only store owners can create products!')
            return redirect(reverse('view_profile'))

    template = 'products/add_product.html'
    context = {
        'form': form
    }
    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """ Edits an existing product the profile has created. """
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product successfully updated!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request,
                           f'Failed to update {product.name},'
                           'please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }
    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ Deletes product from the store if user has access. """
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request,
                     f'{product.name} has been removed from the marketplace.')
    return redirect(reverse('products'))


@login_required
def seller_product_management(request):
    stores = Store.objects.all()
    products = Product.objects.all()
    users = UserProfile.objects.all()

    for user in users:
        if user.user == request.user:
            current_user = user

    my_store = []

    for store in stores:
        if store.user == current_user:
            my_store = store

    template = 'products/seller-product-management.html'
    context = {
        'my_store': my_store,
        'products': products,
    }
    return render(request, template, context)
