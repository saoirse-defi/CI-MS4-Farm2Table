from django.shortcuts import render


def error_handler_404(request, exception):
    print(exception)
    return render(request, '404.html', status=404)


def error_handler_403(request, exception):
    print(exception)
    return render(request, '403.html', status=403)


def error_handler_400(request, exception):
    print(exception)
    return render(request, '400.html', status=400)


def error_handler_500(request):
    return render(request, '500.html', status=500)
