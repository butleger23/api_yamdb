from django.core.exceptions import ValidationError

from .constants import FORBIDDEN_USERNAMES


def validate_forbidden_username(value):
    if value in FORBIDDEN_USERNAMES:
        raise ValidationError(f'Cannot use {value} as a username')
