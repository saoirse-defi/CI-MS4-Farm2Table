import uuid
from django.db import models
from profile.models import UserProfile
from products.models import Product

# Create your models here.


class Wishlist(models.Model):
    wishlist_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserProfile, null=False, blank=False, default=None, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL)

    def __uuid__(self):
        return self.wishlist_id
