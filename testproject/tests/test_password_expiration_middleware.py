from unittest.mock import patch
from datetime import datetime
from datetime import timezone
from datetime import timedelta
from django.test import TestCase
from django.test import override_settings


class PasswordExpirationMiddleware(TestCase):
	def test_新使用者login正常(self):
        user_form = UserCreationForm({
            'username': 'Hana',
            'password1': 'tomay123',
            'password2': 'tomay123',
        })
        user_form.full_clean()
        hana = user_form.save()
        self.client.post(reverse('admin:login'),{
            'username': 'Hana',
            'password': 'tomay123',
        })
        response = self.client.get(reverse('admin:index'))
        self.assertEqual(response.status_code, 200)

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
        with patch(
            'django.utils.timezone.now',
            return_value=datetime(2022, 12, 21, tzinfo=timezone.utc)+timedelta(days=90)
        ):
	        response = self.client.get(reverse('admin:login'))
	        self.assertEqual(response.status_code, 200)

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
	        self.assertEqual(response.url, reverse('admin:setpassword'))
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
