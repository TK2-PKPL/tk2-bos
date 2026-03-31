from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def editor_required(view_func):
    @login_required
    def wrapped(request, *args, **kwargs):
        if request.user.role != "editor":
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapped
