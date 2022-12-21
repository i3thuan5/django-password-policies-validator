from django.test import TestCase
from django.test import override_settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import SetPasswordForm


class RepeatedValidatorTest(TestCase):

    @override_settings(AUTH_PASSWORD_VALIDATORS=[
        {
            'NAME': 'password_policies.password_validation.RepeatedValidator',
        }
    ])
    def test_kāngkhuán密碼袂使khiām第2kái(self):
        user_form = UserCreationForm({
            'username': 'Hana',
            'password1': 'tomay123',
            'password2': 'tomay123',
        })
        hana = user_form.save()
        password_form = SetPasswordForm(user=hana, data={
            'new_password1': 'tomay123',
            'new_password2': 'tomay123',
        })
        self.assertFalse(password_form.is_valid())

    @override_settings(AUTH_PASSWORD_VALIDATORS=[
        {
            'NAME': 'password_policies.password_validation.RepeatedValidator',
        }
    ])
    def test_bôkāngkhuán密碼會使khiām(self):
        user_form = UserCreationForm({
            'username': 'Hana',
            'password1': 'tomay123',
            'password2': 'tomay123',
        })
        hana = user_form.save()
        password_form = SetPasswordForm(user=hana, data={
            'new_password1': 'pawli456',
            'new_password2': 'pawli456',
        })
        self.assertTrue(password_form.is_valid())

    def test_第4kái密碼會使khiāmkah第1kái_kāngkhuán(self):
        self.fail()
    def test_options設做2_第3kái密碼會使khiāmkah第1kái_kāngkhuán(self):
        self.fail()
    def test_options設做0_ài錯誤(self):
        self.fail()
