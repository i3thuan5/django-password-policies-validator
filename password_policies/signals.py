from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist


@receiver(post_save, sender=get_user_model())
def create_password_record(sender, instance, **kwargs):
    try:
        latest_record = instance.password_records.latest()
        if latest_record.password == instance.password:
            return
    except ObjectDoesNotExist:
        pass
    instance.password_records.create(password=instance.password)
