from datetime import timedelta
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.utils import timezone
from django.urls import resolve
from django.urls import reverse


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
            latest_record = request.user.password_records.latest()
            if (timezone.now() - latest_record.date) \
                    >= self.expiration_days:
                if resolve_match.url_name != 'password_change':
                    return redirect(reverse(
                        "admin:password_change",
                        current_app=resolve_match.namespace
                    ))
                messages.warning(
                    request,
                    '已經超過{}工無修改密碼，請修改後才繼續操作'.format(
                        self.expiration_days.days
                    ),
                    fail_silently=True,
                )

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
