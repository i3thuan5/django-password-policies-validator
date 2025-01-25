from django.test import TestCase
from accounts.models import CustomUser


class ComplexityValidatorTest(TestCase):
    def test_the_field_of_password_records_by_custom_model_foregin_keys(self):
        self.assertEqual(
            len(CustomUser.objects.values('id', 'password_records__date')),
            0
        )
