from unittest import TestCase
from django.contrib.auth.models import User


class ComplexityValidatorTest(TestCase):
	def test_lowercase_number(self):
		hana = User.objects.create_user('Hana')
		hana.set_password('tomay123')
		with self.assertRaise('tomay123') as error:
			'大寫、小寫、數字、特殊符號中至少4種字元' in error.objects[0]
