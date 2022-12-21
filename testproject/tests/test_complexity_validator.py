from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


from django.contrib.auth.forms import UserCreationForm

class ComplexityValidatorTest(TestCase):
	def test_lowercase_number_至少4種字元(self):
		hana = User.objects.create_user('Hana')
		userForm = UserCreationForm({
			'username': 'Hana',
			'password1': 'tomay123',
			'password2': 'tomay123',
		})
		userForm.full_clean()
		self.assertTrue(
			userForm.has_error('password1') or userForm.has_error('password2')
		)
