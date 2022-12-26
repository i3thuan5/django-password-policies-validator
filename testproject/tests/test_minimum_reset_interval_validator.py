from unittest.mock import patch
from datetime import datetime
from datetime import timezone
from django.test import TestCase
from django.test import override_settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import SetPasswordForm


class MinimumChangeIntervalValidatorTest(TestCase):
    @override_settings(AUTH_PASSWORD_VALIDATORS=[
        {
            'NAME': 'password_policies.password_validation.MinimumChangeIntervalValidator',  # noqa
        }
    ])
    def test_改了隨改密碼_會擋起來(self):
        user_form = UserCreationForm({
            'username': 'Hana',
            'password1': 'tomay123',
            'password2': 'tomay123',
        })
        user_form.full_clean()
        hana = user_form.save()
        password_form = SetPasswordForm(user=hana, data={
            'new_password1': 'pawli456',
            'new_password2': 'pawli456',
        })
        self.assertFalse(password_form.is_valid())

    @override_settings(AUTH_PASSWORD_VALIDATORS=[
        {
            'NAME': 'password_policies.password_validation.MinimumChangeIntervalValidator',  # noqa
        }
    ])
    def test_過1工後_ētàng改(self):
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
            return_value=datetime(2022, 12, 22, tzinfo=timezone.utc)
        ):
            password_form = SetPasswordForm(user=hana, data={
                'new_password1': 'pawli456',
                'new_password2': 'pawli456',
            })
            self.assertTrue(password_form.is_valid())

    @override_settings(AUTH_PASSWORD_VALIDATORS=[
        {
            'NAME': 'password_policies.password_validation.MinimumChangeIntervalValidator',  # noqa
            'OPTIONS': {
                'min_interval_days': 2.0,
            }
        }
    ])
    def test_options設做2_過1工後改密碼_會擋起來(self):
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
            return_value=datetime(2022, 12, 22, tzinfo=timezone.utc)
        ):
            password_form = SetPasswordForm(user=hana, data={
                'new_password1': 'pawli456',
                'new_password2': 'pawli456',
            })
            self.assertFalse(password_form.is_valid())
