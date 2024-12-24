from django.contrib.auth.models import AbstractUser
from django.db import models


ROLE_CHOICES = (
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),
)

class YamdbUser(AbstractUser):
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        'Роль', default='user', max_length=9, choices=ROLE_CHOICES
    )
    email = models.EmailField('Почта', max_length=254, unique=True)
