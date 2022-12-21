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

    @override_settings(AUTH_PASSWORD_VALIDATORS=[
        {
            'NAME': 'password_policies.password_validation.RepeatedValidator',
        }
    ])
    def test_第4kái袂使kah第1káikāngkhuán_不可以與前三次使用過之密碼相同(self):
        user_form = UserCreationForm({
            'username': 'Hana',
            'password1': 'tomay123',
            'password2': 'tomay123',
        })
        hana = user_form.save()
        SetPasswordForm(user=hana, data={
            'new_password1': 'pawli456',
            'new_password2': 'pawli456',
        }).save()
        SetPasswordForm(user=hana, data={
            'new_password1': 'mali111',
            'new_password2': 'mali111',
        }).save()
        password_form = SetPasswordForm(user=hana, data={
            'new_password1': 'tomay123',
            'new_password2': 'tomay123',
        })
        password_form.save()
        self.assertFalse(password_form.is_valid())

    def test_第5kái密碼會使khiāmkah第1kái_kāngkhuán_不可以與前三次使用過之密碼相同(self):
        user_form = UserCreationForm({
            'username': 'Hana',
            'password1': 'tomay123',
            'password2': 'tomay123',
        })
        hana = user_form.save()
        SetPasswordForm(user=hana, data={
            'new_password1': 'pawli456',
            'new_password2': 'pawli456',
        }).save()
        SetPasswordForm(user=hana, data={
            'new_password1': 'mali111',
            'new_password2': 'mali111',
        }).save()
        SetPasswordForm(user=hana, data={
            'new_password1': '222posi',
            'new_password2': '222posi',
        }).save()
        password_form = SetPasswordForm(user=hana, data={
            'new_password1': 'tomay123',
            'new_password2': 'tomay123',
        })
        password_form.save()
        self.assertTrue(password_form.is_valid())

    def test_options設做2_第3kái密碼會使khiāmkah第1kái_kāngkhuán(self):
        self.fail()
    def test_options設做0_ài錯誤(self):
        self.fail()
