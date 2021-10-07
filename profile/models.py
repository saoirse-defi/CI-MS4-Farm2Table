from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from image_optimizer.fields import OptimizedImageField

from django_countries.fields import CountryField



class UserProfile(models.Model):
    """
    A user profile model for maintaining default
    delivery information and order history.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_phone_number = models.CharField(max_length=20,
                                            null=True, blank=True)
    default_street_address1 = models.CharField(max_length=80,
                                               null=True, blank=True)
    default_street_address2 = models.CharField(max_length=80,
                                               null=True, blank=True)
    default_town = models.CharField(max_length=40,
                                    null=True, blank=True)
    default_county = models.CharField(max_length=80,
                                      null=True, blank=True)
    default_country = CountryField(blank_label='Country',
                                   null=True, blank=True)
    default_postcode = models.CharField(max_length=20,
                                        null=True, blank=True)

    def __str__(self):
        return self.user.username


class SellerProfile(UserProfile):
    organic = models.BooleanField(default=False, null=False, blank=False)
    seller_town = models.CharField(max_length=40,
                                    null=True, blank=True)
    seller_county = models.CharField(max_length=40,
                                    null=True, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default="")
    image = OptimizedImageField(optimized_image_output_size=(400, 300),
                                optimized_image_resize_method='cover',
                                null=True, blank=True)



@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile
    """
    if created:
        UserProfile.objects.create(user=instance)
    # Existing users: just save the profile
    instance.userprofile.save()
