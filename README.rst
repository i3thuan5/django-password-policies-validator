=====
django-password-policies-validator
=====

django-password-policies-validator is a Django app to validate password complexity and prevent users from reusing previous passwords.


Quick start
-----------

1. Add "password_policies" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'polls',
    ]

2. Add 'password_policies.password_validators.ComplexityValidator' to AUTH_PASSWORD_VALIDATORS like this::

    AUTH_PASSWORD_VALIDATORS = [
        ...
        {
            'NAME': 'kuanli.password_validation.ComplexityValidator',
        },
        {
            'NAME': 'kuanli.password_validation.RepeatedValidator',
        },
    ]

3. Run ``python manage.py migrate`` to create the ``PasswordRecord`` models.

4. Start the development server and go to the "Change password" page to check how the new password policies applied.
