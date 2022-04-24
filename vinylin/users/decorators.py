from django.shortcuts import redirect


def anonymous_required(redirect_url='/'):
    def outer(func):
        def wrapper(*args, **kwargs):
            request = args[1]
            if request.user.is_authenticated:
                return redirect(redirect_url)
            return func(*args, **kwargs)
        return wrapper
    return outer
