==================================
django-password-policies-validator
==================================

django-password-policies-validator is a Django app to validate password complexity and prevent users from reusing previous passwords.


Quick start
-----------

#. Add "password_policies" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'password_policies',
    ]

#. Add validators to AUTH_PASSWORD_VALIDATORS setting::

    AUTH_PASSWORD_VALIDATORS = [
        ...
        {
            'NAME': 'password_policies.password_validation.ComplexityValidator',
        },
        {
            'NAME': 'password_policies.password_validation.RepeatedValidator',
        },
        {
            'NAME': 'password_policies.password_validation.MinimumResetIntervalValidator',
        },
    ]

#. Append ``PasswordExpirationMiddleware`` to MIDDLEWARE setting, note that this must be listed **after** the ``'django.contrib.auth.middleware.AuthenticationMiddleware'`` ::

    MIDDLEWARE = [
        ...
        'password_policies.middleware.PasswordExpirationMiddleware',
    ]

#. Run ``python manage.py migrate`` to create the ``PasswordRecord`` models.

#. Start the development server and go to the "Change password" page to check how the new password policies applied.


The ``Validator`` classes
-------------------------

Custom options can be passed into validators by the following syntax ::

    AUTH_PASSWORD_VALIDATORS = [
        ...
        {
            'NAME': 'password_policies.password_validation.ComplexityValidator',
            'OPTIONS': {
                'min_char_types': 3,
                'min_numeric_chars': 2,
            }
        },
    ]

Available options of each validator and their default values are listed below.

``ComplexityValidator(min_char_types=4, min_numeric_chars=1, min_uppercase_chars=1, min_lowercase_chars=1, min_symbol_chars=1)``

    Validates that the password is complex enough by checking how many categories of characters it contains, or the count of certain category of characters. Characters are devided into four categories:

    - Uppercase Latin alphabet characters A-Z
    - Lowercase Latin alphabet characters a-z
    - Digits 0-9
    - Non-alphanumeric (special) characters

    ``min_char_types``
        The minimum categories of characters that the password should contain out of the four categories above. Value should be between 1 and 4 and default to 4.

    ``min_numeric_chars``
        The minimum count of numeric characters that the password should contain. Value should be any positive integer.

    ``min_uppercase_chars``
        The minimum count of uppercase characters that the password should contain. Value should be any positive integer.

    ``min_lowercase_chars``
        The minimum count of lowercase characters that the password should contain. Value should be any positive integer.

    ``min_symbol_chars``
        The minimum count of special characters that the password should contain. Value should be any positive integer.

``RepeatedValidator(record_length=3)``

    Remembers the user's previous *n* passwords and validate the new password doed not repeat any of them.

    ``record_length``
        The number of previous password records that the validator should compare against. Value should be any positive integer.

``MinimumResetIntervalValidator(min_interval=1)``

    Prevent the user from changing the password again within certain period of time. This is to avoid the user to bypass ``RepeatedValidator`` and reuse the old password by changing passwords repeatedly in a short period of time. 

    ``min_interval``
        The minimum time interval (in days) of two consecutive password change attempts. Value should be any positive interger or float.

The ``PasswordExpirationMiddleware`` class
------------------------------------------

``PasswordExpirationMiddleware``

    Checks the user's password-changing records, if the user's password is expired, redirect the user to the password-changing form and shows a warning message.

    This middleware works for any urls under the ``admin`` application namespace and redirects to the ``password_change`` url under the same namespace of the page which the user is redirected from. Urls not under the ``admin`` application namespace are not redirected.

    The password expires in 90 days by default, and the number can be set by providing setting ``PASSWORD_EXPIRATION_DAYS`` to an integer or float value in ``settings.py``.
