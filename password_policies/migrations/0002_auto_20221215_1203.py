# Generated by Django 4.0.7 on 2022-12-15 04:03

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    def create_password_record(apps, schema_editor):
        # We get the model from the versioned app registry;
        # if we directly import it, it'll be the wrong version
        User = apps.get_model(settings.AUTH_USER_MODEL)
        PasswordRecord = apps.get_model("password_policies", "PasswordRecord")

        for user in User.objects.all():
            PasswordRecord.objects.create(user=user, password=user.password)

    dependencies = [
        ('password_policies', '0001_initial'),
    ]

    operations = [migrations.RunPython(create_password_record)]
