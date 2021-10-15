from django.contrib import admin
from .models import Wishlist


class WishlistAdmin(admin.ModelAdmin):
    list_display = (
        'wishlist_id',
        'user',
        'sku'
    )

    ordering = ('wishlist_id',)


admin.site.register(Wishlist)
