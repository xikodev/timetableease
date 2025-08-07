from django.shortcuts import redirect


def admin_required(redirect_page):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            user_object = request.user

            if user_object.is_superuser:
                return view_func(request, *args, **kwargs)
            else:
                return redirect(redirect_page)
        return wrapper_func
    return decorator


def group_required(redirect_page):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            user_object = request.user

            if user_object.is_superuser or user_object.groups.all():
                return view_func(request, *args, **kwargs)
            else:
                return redirect(redirect_page)
        return wrapper_func
    return decorator
