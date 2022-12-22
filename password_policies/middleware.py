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

        from django.urls import resolve
        from django.urls import reverse
        resolve_match = resolve(request.path)
        print(
            'resolve_match',
            resolve_match.url_name,
            resolve_match.view_name,

            )
        print('app_name',resolve_match.app_name,'namespace',resolve_match.namespace)
        print(
            "request.path.startswith(reverse('admin:index'))",
            request.path.startswith(reverse('admin:index'))
            )
        if request.user.is_authenticated:
            if resolve_match.app_name == 'admin':
                latest_password_record = request.user.password_records.latest('date')
                if (timezone.now() - latest_password_record.date) \
                    >= self.expiration_days:
                    return redirect('{}:password_change'.format(resolve_match.namespace))

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response