import uuid
from django.db import models
from django_countries.fields import CountryField

from profile.models import UserProfile


# Create your models here.


class Store(models.Model):
    store_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                editable=False)
    user = models.ForeignKey(UserProfile, null=True, blank=False,
                             default=None, on_delete=models.CASCADE)
    name = models.CharField(max_length=254)
    description = models.TextField(max_length=1024, blank=False, default="")
    email = models.CharField(max_length=254)
    phone_number = models.CharField(max_length=20,
                                    null=True, blank=True)
    iban = models.CharField(max_length=34,
                            null=True, blank=True)
    street_address1 = models.CharField(max_length=80,
                                       null=True, blank=True)
    street_address2 = models.CharField(max_length=80,
                                       null=True, blank=True)
    town = models.CharField(max_length=40,
                            null=True, blank=True)
    county = models.ForeignKey('store.County',
                               on_delete=models.SET_NULL,
                               null=True, blank=True)
    country = CountryField(blank_label='Country',
                           null=True, blank=True)
    postcode = models.CharField(max_length=20,
                                null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    organic = models.BooleanField(default=False, null=False, blank=False)
    rating = models.DecimalField(max_digits=6, decimal_places=2,
                                 null=True, blank=True)

    def __str__(self):
        return str(self.name)


class County(models.Model):
    verbose_name_plural = 'Counties'

    name = models.CharField(max_length=254, blank=False)

    def __str__(self):
        return str(self.name)
