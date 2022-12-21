from django.test import TestCase
from django.test import override_settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import SetPasswordForm


class MinimumResetIntervalValidatorTest(TestCase):
    @override_settings(AUTH_PASSWORD_VALIDATORS=[
        {
            'NAME':
            'password_policies.password_validation.MinimumResetIntervalValidator',
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

    def test_過1工後_ētàng改(self):
        self.fail()
    def test_options設做2_過1工後改密碼_會擋起來(self):
        self.fail()
