from django.apps import AppConfig


class PasswordPoliciesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'password_policies'

    def ready(self):
        # Implicitly connect signal handlers decorated with @receiver.
        from . import signals  # noqa
