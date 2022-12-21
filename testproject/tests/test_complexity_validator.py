from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError



class ComplexityValidatorTest(TestCase):
	def test_lowercase_number(self):
		hana = User.objects.create_user('Hana')
		with self.assertRaises(ValidationError, hana.set_password, 'tomay123') as error:
			'大寫、小寫、數字、特殊符號中至少4種字元' in error.objects[0]
