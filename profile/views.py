from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import UserProfile
from .forms import UserProfileForm


@login_required
def profile(request):
    """Displays user profile."""
    profile = get_object_or_404(UserProfile, user=request.user)

    form = UserProfileForm(instance=profile)
    orders = profile.orders.all()
    template = "profile/profile.html"
    context = {
        'form': form,
        'orders': orders,
    }

    return render(request, template, context)
