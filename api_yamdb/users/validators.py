from django.core.exceptions import ValidationError


def validate_username_me(value):
    if value == 'me':
        raise ValidationError('Cannot use "me" as a username')
