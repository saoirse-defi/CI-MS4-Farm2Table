from django.shortcuts import render


def profile(request):
    """Displays user profile."""
    template = "profile/profile.html"
    context = {}

    return render(request, template, context)
