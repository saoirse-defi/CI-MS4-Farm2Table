import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from image_optimizer.fields import OptimizedImageField
from django_countries.fields import CountryField

from profile.models import UserProfile


# Create your models here.


class Store(models.Model):
    store_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserProfile, null=True, blank=False, default=None, on_delete=models.CASCADE)
    name = models.CharField(max_length=254)
    email = models.CharField(max_length=254)
    phone_number = models.CharField(max_length=20,
                                            null=True, blank=True)
    street_address1 = models.CharField(max_length=80,
                                               null=True, blank=True)
    street_address2 = models.CharField(max_length=80,
                                               null=True, blank=True)
    town = models.CharField(max_length=40,
                                    null=True, blank=True)
    county = models.CharField(max_length=80,
                                      null=True, blank=True)
    country = CountryField(blank_label='Country',
                                   null=True, blank=True)
    postcode = models.CharField(max_length=20,
                                        null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = OptimizedImageField(optimized_image_output_size=(400, 300),
                                optimized_image_resize_method='cover',
                                null=True, blank=True)
    organic = models.BooleanField(default=False, null=False, blank=False)
    iban = models.CharField(max_length=64, null=True, blank=True)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name
