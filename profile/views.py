from django.shortcuts import render, get_object_or_404, reverse
from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    login,
    logout,
)
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from .models import UserProfile
from .forms import UserProfileForm, UserLoginForm, UserRegisterForm
from checkout.models import Order
from store.models import Store


def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect(reverse('view_profile'))

    context = {
        'form': form,
    }
    return render(request, "profile/login.html", context)


def signup_view(request):
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        return redirect(reverse('view_profile'))

    context = {
        'form': form,
    }
    return render(request, "profile/signup.html", context)


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def view_profile(request):
    """Displays user profile."""
    profile = get_object_or_404(UserProfile, user=request.user)
    form = UserProfileForm(instance=profile)
    current_user = UserProfile.objects.get(user=request.user)

    try:
        store = Store.objects.get(user=current_user)
    except Exception as e:
        store = None
        print(e)

    orders = Order.objects.all().filter(user_profile=profile)

    template = "profile/profile.html"
    context = {
        'orders': orders,
        'store': store,
        'on_profile_page': True,
        'profile': profile,
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect(reverse('view_profile'))
        else:
            messages.error(request,
                           'Profile Update Failed: '
                           'Please ensure the form is valid.')
    else:
        form = UserProfileForm(instance=profile)

    template = "profile/profile.html"
    context = {
        'form': form,
        'profile': profile,
    }

    return render(request, template, context)


@login_required
def order_history(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is a past confirmation for order { order_number }.'
        'A confirmation email was sent once the order was placed.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)
