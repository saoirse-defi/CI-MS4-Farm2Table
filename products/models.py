import uuid
from django.db import models

from store.models import Store


class Category(models.Model):
    category_id = models.UUIDField(primary_key=True,
                                   default=uuid.uuid4, editable=False)
    verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    sku = models.UUIDField(primary_key=True,
                           default=uuid.uuid4,
                           editable=False)
    seller_store = models.ForeignKey(Store,
                                     null=True,
                                     blank=False,
                                     default=None,
                                     on_delete=models.CASCADE)
    category = models.ForeignKey(Category,
                                 null=True,
                                 blank=True,
                                 on_delete=models.SET_NULL)
    name = models.CharField(max_length=254)
    description = models.TextField()
    organic = models.BooleanField(default=False, null=False, blank=False)
    has_sizes = models.BooleanField(default=True, null=False, blank=False)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=6, decimal_places=2,
                                 null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name
