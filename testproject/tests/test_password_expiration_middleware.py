from unittest.mock import patch
from datetime import datetime
from datetime import timezone
from datetime import timedelta
from django.test import TestCase
from django.test import override_settings
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import SetPasswordForm
from django.urls import reverse
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.urls import path


class PasswordExpirationMiddleware(TestCase):
    @override_settings(MIDDLEWARE=settings.MIDDLEWARE + [
        'password_policies.middleware.PasswordExpirationMiddleware',
    ])
    def test_新使用者login正常(self):
        user_form = UserCreationForm({
            'username': 'Hana',
            'password1': 'tomay123',
            'password2': 'tomay123',
        })
        user_form.full_clean()
        hana = user_form.save()
        hana.is_active = True
        hana.is_staff = True
        hana.save()
        self.client.post(reverse('admin:login'),{
            'username': 'Hana',
            'password': 'tomay123',
        })
        response = self.client.get(reverse('admin:index'))
        self.assertEqual(response.status_code, 200)

    @override_settings(MIDDLEWARE=settings.MIDDLEWARE + [
        'password_policies.middleware.PasswordExpirationMiddleware',
    ])
    def test_新使用者過90工攏無改密碼_tī登入頁正常顯示(self):
        with patch(
            'django.utils.timezone.now',
            return_value=datetime(2022, 12, 21, tzinfo=timezone.utc)
        ):
            user_form = UserCreationForm({
                'username': 'Hana',
                'password1': 'tomay123',
                'password2': 'tomay123',
            })
            user_form.full_clean()
            hana = user_form.save()
            hana.is_active = True
            hana.is_staff = True
            hana.save()
        with patch(
            'django.utils.timezone.now',
            return_value=datetime(2022, 12, 21, tzinfo=timezone.utc)+timedelta(days=90)
        ):
            response = self.client.get(reverse('admin:login'))
            self.assertEqual(response.status_code, 200)

    @override_settings(MIDDLEWARE=settings.MIDDLEWARE + [
        'password_policies.middleware.PasswordExpirationMiddleware',
    ])
    def test_新使用者過90工攏無改密碼_會到重設密碼ê網頁(self):
        with patch(
            'django.utils.timezone.now',
            return_value=datetime(2022, 12, 21, tzinfo=timezone.utc)
        ):
            user_form = UserCreationForm({
                'username': 'Hana',
                'password1': 'tomay123',
                'password2': 'tomay123',
            })
            user_form.full_clean()
            hana = user_form.save()
            hana.is_active = True
            hana.is_staff = True
            hana.save()
        with patch(
            'django.utils.timezone.now',
            return_value=datetime(2022, 12, 21, tzinfo=timezone.utc)+timedelta(days=90)
        ):
            self.client.post(reverse('admin:login'),{
                'username': 'Hana',
                'password': 'tomay123',
            })
            response = self.client.get(reverse('admin:index'))
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, reverse('admin:password_change'))

    @override_settings(MIDDLEWARE=settings.MIDDLEWARE + [
        'password_policies.middleware.PasswordExpirationMiddleware',
    ])
    def test_使用者改過密碼_tī90工內正常登入(self):
        with patch(
            'django.utils.timezone.now',
            return_value=datetime(2022, 12, 21, tzinfo=timezone.utc)
        ):
            user_form = UserCreationForm({
                'username': 'Hana',
                'password1': 'tomay123',
                'password2': 'tomay123',
            })
            user_form.full_clean()
            hana = user_form.save()
            hana.is_active = True
            hana.is_staff = True
            hana.save()
        with patch(
            'django.utils.timezone.now',
            return_value=datetime(2022, 12, 21, tzinfo=timezone.utc)+timedelta(days=30)
        ):
            password_form = SetPasswordForm(user=hana, data={
                'new_password1': 'pawli456',
                'new_password2': 'pawli456',
            })
            password_form.full_clean()
            password_form.save()
        with patch(
            'django.utils.timezone.now',
            return_value=datetime(2022, 12, 21, tzinfo=timezone.utc)+timedelta(days=90)
        ):
            self.client.post(reverse('admin:login'),{
                'username': 'Hana',
                'password': 'pawli456',
            })
            response = self.client.get(reverse('admin:index'))
            self.assertEqual(response.status_code, 200)

    @override_settings(MIDDLEWARE=settings.MIDDLEWARE + [
        'password_policies.middleware.PasswordExpirationMiddleware',
    ], PASSWORD_EXPIRATION_DAYS=180.0)
    def test_options設做180_tī90工正常登入(self):
        with patch(
            'django.utils.timezone.now',
            return_value=datetime(2022, 12, 21, tzinfo=timezone.utc)
        ):
            user_form = UserCreationForm({
                'username': 'Hana',
                'password1': 'tomay123',
                'password2': 'tomay123',
            })
            user_form.full_clean()
            hana = user_form.save()
            hana.is_active = True
            hana.is_staff = True
            hana.save()
        with patch(
            'django.utils.timezone.now',
            return_value=datetime(2022, 12, 21, tzinfo=timezone.utc)+timedelta(days=90)
        ):
            self.client.post(reverse('admin:login'),{
                'username': 'Hana',
                'password': 'tomay123',
            })
            response = self.client.get(reverse('admin:index'))
            self.assertEqual(response.status_code, 200)

    @override_settings(MIDDLEWARE=settings.MIDDLEWARE + [
        'password_policies.middleware.PasswordExpirationMiddleware',
    ], ROOT_URLCONF='tests.test_password_expiration_middleware')
    def test_admin是別ê名(self):
        with patch(
            'django.utils.timezone.now',
            return_value=datetime(2022, 12, 21, tzinfo=timezone.utc)
        ):
            user_form = UserCreationForm({
                'username': 'Hana',
                'password1': 'tomay123',
                'password2': 'tomay123',
            })
            user_form.full_clean()
            hana = user_form.save()
            hana.is_active = True
            hana.is_staff = True
            hana.save()
        with patch(
            'django.utils.timezone.now',
            return_value=datetime(2022, 12, 21, tzinfo=timezone.utc)+timedelta(days=90)
        ):
            self.client.post(reverse('autai:login'),{
                'username': 'Hana',
                'password': 'tomay123',
            })
            response = self.client.get(reverse('autai:index'))
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, reverse('autai:password_change'))


autai_site=AdminSite(name='autai')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('autai/', autai_site.urls),
]
