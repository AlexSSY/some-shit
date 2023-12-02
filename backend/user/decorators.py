from functools import wraps
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions


def email_verified(view_function):
    @wraps(view_function)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.email_verified:
            raise exceptions.AuthenticationFailed(detail=_('email is not verified'))
        return view_function(request, *args, **kwargs)
    return _wrapped_view
