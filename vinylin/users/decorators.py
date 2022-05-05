from django.shortcuts import redirect
from django.urls import reverse_lazy


index_url = reverse_lazy('index')


def anonymous_only(redirect_url=index_url):
    def outer(func):
        def wrapper(*args, **kwargs):
            request = args[1]
            if request.user.is_authenticated:
                return redirect(redirect_url)
            return func(*args, **kwargs)
        return wrapper
    return outer
