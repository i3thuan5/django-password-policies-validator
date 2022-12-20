from django.db import models
from django.conf import settings


class PasswordRecord(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='password_records',
        on_delete=models.CASCADE,
        editable=False
    )

    # max_length 參考 django.contrib.auth.base_user.AbstractBaseUser.password
    password = models.CharField(
        'Password hash',
        max_length=128,
        editable=False
    )
    date = models.DateTimeField(
        'Date',
        auto_now_add=True,
        editable=False
    )
