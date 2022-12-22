from datetime import timedelta
from django.conf import settings
from django.shortcuts import redirect
from django.utils import timezone
from django.urls import resolve


class PasswordExpirationMiddleware:
    def __init__(self, get_response):
        # One-time configuration and initialization.
        self.get_response = get_response
        self.expiration_days = timedelta(
            days=getattr(settings, 'PASSWORD_EXPIRATION_DAYS', 90.0)
        )

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        resolve_match = resolve(request.path)
        if resolve_match.app_name == 'admin' and request.user.is_authenticated:
            if resolve_match.url_name != 'password_change':
                latest_password_record = request.user.password_records.latest('date')
                if (timezone.now() - latest_password_record.date) \
                    >= self.expiration_days:
                    return redirect('{}:password_change'.format(resolve_match.namespace))

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response