from unittest.mock import patch
from unittest import skip
from datetime import datetime
from datetime import timezone
from datetime import timedelta
from django.test import TestCase
from django.test import override_settings
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import SetPasswordForm
from django.urls import reverse


@override_settings(MIDDLEWARE=settings.MIDDLEWARE + [
    'password_policies.middleware.PasswordExpirationMiddleware',
])
class PasswordExpirationMiddleware(TestCase):
    user_creation_date = datetime(2022, 12, 21, tzinfo=timezone.utc)

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
        self.client.post(reverse('admin:login'), {
            'username': 'Hana',
            'password': 'tomay123',
        })
        response = self.client.get(reverse('admin:index'))
        self.assertEqual(response.status_code, 200)

    def test_新使用者過90工攏無改密碼_tī登入頁正常顯示(self):
        with patch(
            'django.utils.timezone.now',
            return_value=self.user_creation_date
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
            return_value=self.user_creation_date + timedelta(days=90)
        ):
            response = self.client.get(reverse('admin:login'))
            self.assertEqual(response.status_code, 200)

    def test_新使用者過90工攏無改密碼_會到重設密碼ê網頁(self):
        with patch(
            'django.utils.timezone.now',
            return_value=self.user_creation_date
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
            return_value=self.user_creation_date + timedelta(days=90)
        ):
            self.client.post(reverse('admin:login'), {
                'username': 'Hana',
                'password': 'tomay123',
            })
            response = self.client.get(reverse('admin:index'))
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, reverse('admin:password_change'))

    def test_新使用者過90工攏無改密碼_重設密碼網頁有提示(self):
        with patch(
            'django.utils.timezone.now',
            return_value=self.user_creation_date
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
            return_value=self.user_creation_date + timedelta(days=90)
        ):
            response1 = self.client.get(reverse('admin:index'))
            response2 = self.client.post(response1.url, {  # login
                'username': 'Hana',
                'password': 'tomay123',
            })
            response3 = self.client.get(response2.url)  # index
            response4 = self.client.get(response3.url)  # password_change
            self.assertEqual(len(response4.context['messages']), 1, response4.context['messages'])

    def test_新使用者過90工攏無改密碼_重設密碼有作用(self):
        with patch(
            'django.utils.timezone.now',
            return_value=self.user_creation_date
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
            return_value=self.user_creation_date + timedelta(days=90)
        ):
            self.client.post(reverse('admin:login'), {
                'username': 'Hana',
                'password': 'tomay123',
            })
            response1 = self.client.get(reverse('admin:password_change'))
            self.assertEqual(response1.status_code, 200)
            response2 = self.client.post(reverse('admin:password_change'), {
                    'old_password': 'tomay123',
                    'new_password1': ':posi:333',
                    'new_password2': ':posi:333',
            })
            self.assertEqual(
                response2.status_code, 302, response2.content.decode()
            )
            self.assertEqual(
                response2.url, reverse('admin:password_change_done')
            )
            response3 = self.client.get(reverse('admin:index'))
            self.assertEqual(response3.status_code, 200, response3)

    def test_使用者改過密碼_tī90工內正常登入(self):
        with patch(
            'django.utils.timezone.now',
            return_value=self.user_creation_date
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
            return_value=self.user_creation_date + timedelta(days=30)
        ):
            password_form = SetPasswordForm(user=hana, data={
                'new_password1': 'pawli456',
                'new_password2': 'pawli456',
            })
            password_form.full_clean()
            password_form.save()
        with patch(
            'django.utils.timezone.now',
            return_value=self.user_creation_date + timedelta(days=90)
        ):
            self.client.post(reverse('admin:login'), {
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
            return_value=self.user_creation_date
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
            return_value=self.user_creation_date + timedelta(days=90)
        ):
            self.client.post(reverse('admin:login'), {
                'username': 'Hana',
                'password': 'tomay123',
            })
            response = self.client.get(reverse('admin:index'))
            self.assertEqual(response.status_code, 200)

    def test_admin是別ê名(self):
        with patch(
            'django.utils.timezone.now',
            return_value=self.user_creation_date
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
            return_value=self.user_creation_date + timedelta(days=90)
        ):
            self.client.post(reverse('autai:login'), {
                'username': 'Hana',
                'password': 'tomay123',
            })
            response = self.client.get(reverse('autai:index'))
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, reverse('autai:password_change'))

    def test_admin以外ê網頁_正常顯示(self):
        with patch(
            'django.utils.timezone.now',
            return_value=self.user_creation_date
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
            return_value=self.user_creation_date + timedelta(days=90)
        ):
            # 後台有登入
            self.client.post(reverse('admin:login'), {
                'username': 'Hana',
                'password': 'tomay123',
            })
            # 前台看網站
            response = self.client.get(reverse('custom_index'))
            self.assertEqual(response.status_code, 200)

    @skip('以後有需求才定義')
    @override_settings(MIDDLEWARE=settings.MIDDLEWARE + [
        'password_policies.middleware.PasswordExpirationMiddleware',
    ], PASSWORD_CHANGE_REDIRECT_TO='custom_password_change')
    def test_tīadmin外口_ài跳去指定êview(self):
        self.fail()
