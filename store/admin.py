from django.contrib import admin
from .models import Store, County

# Register your models here.


class StoreAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'name'
    )

    ordering = ('name',)


class CountyAdmin(admin.ModelAdmin):
    list_display = (
        'friendy_name',
        'name'
    )

    ordering = ('name',)


admin.site.register(County)
admin.site.register(Store)