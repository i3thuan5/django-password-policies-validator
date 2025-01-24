from django.test import TestCase
from accounts.models import CustomUser


class ComplexityValidatorTest(TestCase):
    def test_use_custom_model_foregin_keys(self):
        self.assertEqual(
            len(CustomUser.objects.values('id', 'password_records_id')),
            0
        )
