from django.test import TestCase
from django.test import override_settings
from django.contrib.auth.forms import UserCreationForm


class ComplexityValidatorTest(TestCase):
    def test_lowercase_number_2種字元(self):
        user_form = UserCreationForm({
            'username': 'Hana',
            'password1': 'tomay123',
            'password2': 'tomay123',
        })
        self.assertFalse(user_form.is_valid())

    def test_4種字元(self):
        user_form = UserCreationForm({
            'username': 'Hana',
            'password1': 'toMay!23',
            'password2': 'toMay!23',
        })
        self.assertTrue(user_form.is_valid())

    @override_settings(AUTH_PASSWORD_VALIDATORS=[
        {
            'NAME':
            'password_policies.password_validation.ComplexityValidator',
            'OPTIONS': {
                'min_char_types': 2,
                'min_numeric_chars': 2,
                'min_uppercase_chars': 0,
                'min_lowercase_chars': 2,
                'min_symbol_chars': 0,
            },
        }
    ])
    def test_lowercase_number_2種字元就好(self):
        user_form = UserCreationForm({
            'username': 'Hana',
            'password1': 'tomay123',
            'password2': 'tomay123',
        })
        self.assertTrue(user_form.is_valid())

    @override_settings(AUTH_PASSWORD_VALIDATORS=[
        {
            'NAME':
            'password_policies.password_validation.ComplexityValidator',
            'OPTIONS': {
                'min_char_types': 2,
                'min_numeric_chars': 5,
                'min_uppercase_chars': 0,
                'min_lowercase_chars': 2,
                'min_symbol_chars': 0,
            },
        }
    ])
    def test_length(self):
        user_form = UserCreationForm({
            'username': 'Hana',
            'password1': 'tomay123',
            'password2': 'tomay123',
        })
        self.assertFalse(user_form.is_valid())
