from django.contrib.auth.models import AbstractUser
from django.db import models


ROLE_CHOICES = (
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),
)

LONGEST_ROLE_LENGTH = len('moderator')


class YamdbUser(AbstractUser):
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        'Роль',
        default='user',
        max_length=LONGEST_ROLE_LENGTH,
        choices=ROLE_CHOICES,
    )
    email = models.EmailField('Почта', max_length=254, unique=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['id']

    def __str__(self):
        return self.username
