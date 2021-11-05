from .models import Store


def store_context(request):
    stores = Store.objects.all()

    return {'stores': stores}