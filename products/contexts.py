from .models import Category


def category_context(request):
    categories = Category.object.all()

    return {'categories': categories}
