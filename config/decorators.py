from functools import wraps
from django.shortcuts import redirect, render


def unauthenticated_user(view_func):
    @wraps(view_func)
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper_func(request, *args, **kwargs):
            group = request.user.groups.values_list('name', flat=True).first()
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            return render(request, 'home/404.html', status=403)
        return wrapper_func
    return decorator