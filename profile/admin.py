from django.contrib import admin
from .models import UserProfile, County

# Register your models here.

class CountyAdmin(admin.ModelAdmin):
    list_display = (
        'friendy_name',
        'name'
    )

    ordering = ('name',)


admin.site.register(UserProfile)
admin.site.register(County)
