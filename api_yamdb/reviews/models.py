from django.contrib.auth.models import AbstractUser
from django.db import models

ROLE_CHOICES = (
    ('admin', 'Администратор'),
    ('user', 'Аутентифицированный пользователь'),
    ('moderator', 'Модератор'),
)


class User(AbstractUser):
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль',
        max_length=50,
        choices=ROLE_CHOICES,
    )
