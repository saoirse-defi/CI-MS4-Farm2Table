from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from django.contrib.auth.decorators import login_required

from .filters import ProductFilter
from .models import Product, Category
from .forms import ProductForm
from profile.models import UserProfile
from store.models import Store
from wishlist.models import Wishlist

# Custom Decorators


def superuser_required(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.error(request, 'Sorry only store owners can do that.')
            return redirect(reverse('error_handler_500'))
        else:
            return func(request)
    return wrapper


def store_required(func):
    def wrapper(request, *args, **kwargs):
        try:
            user = UserProfile.objects.filter(user=request.user)
            store = Store.objects.filter(user=user)
        except Exception as e:
            user = None
            store = None

        if store is not None:
            return func(request)
        else:
            messages.error(request,
                           "Only store owners can create & sell products.")
            return redirect(reverse('products'))
    return wrapper


def store_owner_required(func, product_id):
    def wrapper(request, *args, **kwargs):
        product = Product.objects.filter(sku=product_id)
        try:
            user = UserProfile.objects.filter(user=request.user)
            store = Store.objects.filter(user=user)
        except Exception as e:
            user = None
            store = None

        if store is not None:
            if product.seller_store != store:
                return func(request, *args, **kwargs)
            else:
                messages.error(request,
                            "You can only edit your own products.")
                return redirect(reverse('products'))
        else:
            messages.error(request,
                           "Only store owners can edit products.")
    return wrapper


# Product Views

def all_products(request):
    """ A view to handle all products """

    products = Product.objects.all()
    product_filter = ProductFilter(request.GET, queryset=products)
    products = product_filter.qs

    if request.user.is_authenticated:
        current_user = UserProfile.objects.get(user=request.user)
        current_wishlist = Wishlist.objects.all().filter(user=current_user)

        context = {
            'products': products,
            'product_filter': product_filter,
            'current_wishlist': current_wishlist,
            'current_user': current_user,
        }

        return render(request, 'products/products.html', context)
    else:
        context = {
            'products': products,
            'product_filter': product_filter,
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
    wishlist_id = None

    try:
        current_user = UserProfile.objects.get(user=request.user)
    except Exception as e:
        current_user = None
        print(e)

    product = get_object_or_404(Product, pk=product_id)
    store = get_object_or_404(Store, pk=product.seller_store.store_id)

    if current_user is not None:
        try:
            current_wishlist = Wishlist.objects.all().filter(user=current_user)
            for wish in current_wishlist:
                if wish.product == product:
                    wishlist_id = wish.wishlist_id
        except Exception as e:
            wishlist_id = None
            print(e)

        if store.user == current_user:
            context = {
                'wishlist_id': wishlist_id,
                'current_user': current_user,
                'product': product,
                'store': store,
                }
            return render(request, 'products/product_detail.html', context)
        else:
            context = {
                'wishlist_id': wishlist_id,
                'current_user': current_user,
                'product': product,
                'store': store,
                }
            return render(request,
                          'products/product_detail_anon.html',
                          context)
    else:
        context = {
            'product': product,
            'store': store,
            }
        return render(request, 'products/product_detail_anon.html', context)


@store_required
@login_required
# @superuser_required
def add_product(request):
    """ Add a product to the store. """
    try:
        current_user = UserProfile.objects.get(user=request.user)
        my_store = Store.objects.get(user=current_user)
    except Exception as e:
        current_user = None
        my_store = None
        print(e)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if my_store is not None:
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
        messages.error(request,
                       'You cannot add a product to this '
                       'store as you are not the owner.')
    else:
        form = ProductForm(request.POST)

    template = 'products/add_product.html'
    context = {
        'form': form
    }
    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """ Edits an existing product the profile has created. """
    try:
        current_user = UserProfile.objects.get(user=request.user)
        my_store = Store.objects.get(user=current_user)
    except Exception as e:
        current_user = None
        my_store = None
        print(e)

    product = get_object_or_404(Product, pk=product_id)
    if product.seller_store == my_store:
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES, instance=product)
            if form.is_valid():
                form.save()
                messages.success(request, 'Product successfully updated!')
                return redirect(reverse('product_detail', args=[product_id]))
            else:
                messages.error(request,
                               f'Failed to update {product.name}, '
                               'please ensure the form is valid.')
        else:
            form = ProductForm(instance=product)
            messages.info(request, f'You are editing {product.name}')
    else:
        messages.error(request, 'You can only edit your own products.')
        return redirect(reverse('products'))

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }
    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ Deletes product from the store if user has access. """
    try:
        current_user = UserProfile.objects.get(user=request.user)
        my_store = Store.objects.get(user=current_user)
    except Exception as e:
        current_user = None
        my_store = None
        print(e)

    product = get_object_or_404(Product, pk=product_id)
    if product.seller_store == my_store:
        product.delete()
        messages.success(request,
                         f'{product.name} has been '
                         'removed from the marketplace.')
        return redirect(reverse('products'))
    else:
        messages.error(request,
                       f'{product.name} cannot be deleted '
                       'as you do not have the authority.')
        return redirect(reverse('products'))


@store_required
@login_required
def seller_product_management(request):
    try:
        current_user = UserProfile.objects.get(user=request.user)
        my_store = Store.objects.get(user=current_user)
    except Exception as e:
        current_user = None
        my_store = None
        print(e)

    products = Product.objects.filter(seller_store=my_store)

    template = 'products/seller-product-management.html'
    context = {
        'my_store': my_store,
        'products': products,
        'current_user': current_user,
    }
    return render(request, template, context)
