from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model


@receiver(post_save, sender=get_user_model())
def create_password_record(sender, instance, **kwargs):
    instance.password_records.create(password=instance.password)
