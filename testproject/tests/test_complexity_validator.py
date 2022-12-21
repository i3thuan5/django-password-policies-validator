from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


from django.contrib.auth.forms import UserCreationForm

class ComplexityValidatorTest(TestCase):
	def test_lowercase_number(self):
		hana = User.objects.create_user('Hana')
		userForm = UserCreationForm({
			'username': 'Hana',
			'password1': 'tomay123',
			'password2': 'tomay123',
		})
		with self.assertRaises(ValidationError, userForm.full_clean) as error:
			'大寫、小寫、數字、特殊符號中至少4種字元' in error.objects[0]
