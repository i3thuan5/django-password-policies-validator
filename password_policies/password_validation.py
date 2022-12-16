from django.core.exceptions import ValidationError
import re


SYMBOLS = re.compile(r'[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]')


class ComplexityValidator:
    def __init__(self, **kwargs):
        self.min_char_types = kwargs.pop('min_char_types', 4)
        self.min_chars_of_each_type = [
            ('min_numeric_chars', r'[0-9]'),
            ('min_uppercase_chars', r'[A-Z]'),
            ('min_lowercase_chars', r'[a-z]'),
            ('min_symbol_chars', SYMBOLS),
        ]
        for attr, _regex in self.min_chars_of_each_type:
            setattr(
                self, attr,
                kwargs.get(attr, 1)
            )

    def validate(self, password, user=None):
        password_valid = True
        errors = []
        for type_, regex in self.min_chars_of_each_type:
            char_types_contained = 0
            find = re.findall(regex, password)
            required = getattr(self, type_)
            if len(find) < required:
                password_valid = False
                errors.append(f"至少{required}個{type_}字元")
            if find:
                char_types_contained += 1

        if char_types_contained < self.min_char_types:
            password_valid = False
            errors.append(f"大寫、小寫、數字、特殊符號中至少{self.min_char_types}種字元")

        if not password_valid:
            raise ValidationError(
                f"密碼應包含{'；'.join(errors)}。",
                code='password_lacks_numeric_or_symbols',
            )

    def get_help_text(self):
        requirements = []
        for type_, regex in self.min_chars_of_each_type:
            required = getattr(self, type_)
            if required:
                requirements.append(f"至少{required}個{type_}字元")
        if self.min_char_types:
            requirements.append(
                f"大寫、小寫、數字、特殊符號中至少{self.min_char_types}種字元"
            )

        return f"密碼應包含{'；'.join(requirements)}。"
