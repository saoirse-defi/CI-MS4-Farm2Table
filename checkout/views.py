from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    bag = request.session.get('bag', {})

    if not bag:
        messages.error(request, "Nothing yet to see in your cart!")
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51JUBLoJiiZl6riemjloDASbxq8eXcDOPrvAe0Tbi9ng0uW4S9LIjwX6r44r4a0Qv0W7u3zea0dlD5akWTk7FvBDd00grgIGrUr',
        'client_secret': 'sk_test_51JUBLoJiiZl6riemDFRe7fWLn30zGHnPhTr71v9nk1o8pXyiGPo5AiyC9JHaUhurlyNeorizwkGZ8RxPVsDw5hwF00IYWXXp4U'
    }

    return render(request, template, context)
