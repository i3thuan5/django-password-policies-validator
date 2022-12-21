from datetime import timedelta
from django.conf import settings
from django.shortcuts import redirect
from django.utils import timezone


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

        if request.user.is_authenticated:
            latest_password_record = request.user.password_records.latest('date')
            if (timezone.now() - latest_password_record.date) \
                >= self.expiration_days:
                return redirect('admin:password_change')

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response