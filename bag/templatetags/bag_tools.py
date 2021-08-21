from decimal import Decimal
from django import template
from django.template.defaultfilters import stringfilter


register = template.Library()


@register.filter(name='calc_subtotal')
def calc_subtotal(price, quantity):
    return price * quantity


@register.filter(name='calc_total_with_size')
@stringfilter
def calc_total_with_size(total, size):
    return Decimal(total) * (Decimal(size)/250)
