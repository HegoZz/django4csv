from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


def validate_year(value):
    current_year = datetime.now().year
    if -3400 > value or value > current_year:
        raise ValidationError(
            _('На данный момент нет произведений, '
              'созданных в %(value)-м году'),
            params={'value': value},
        )


def validate_score(value):
    if 0 > value or value > 10:
        raise ValidationError('Оценка должна быть от 0 до 10')


class Roles(models.Model):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLE_CHOICES = (
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
        (USER, 'Аутентифицированный пользователь'),
    )


class User(AbstractUser):
    """Кастомизация модели пользователя."""
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=50,
        choices=Roles.ROLE_CHOICES,
        default='user'
    )
    email = models.EmailField(
        verbose_name='Email',
        max_length=100,
        unique=True,
    )

    @property
    def is_admin(self):
        return self.role == Roles.ADMIN

    @property
    def is_moderator(self):
        return self.role == Roles.MODERATOR

    @property
    def is_user(self):
        return self.role == Roles.USER

    class Meta:
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователи'


class Group(models.Model):
    """Описание модели группы."""
    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
    
    vkId = models.PositiveIntegerField(
        verbose_name='ID группы',
        unique=True,
    )
    updated = models.DateTimeField(verbose_name='Дата обновления')
    type = models.CharField(
        verbose_name='Тип',
        max_length=42,
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=73,
    )
    screenName = models.SlugField(
        verbose_name='Уникальный идентификатор',
        max_length=73,
        unique=True,
    )
    photo = models.URLField(
        blank=True,
        null=True,
    )
    cover = models.URLField(
        blank=True,
        null=True,
    )
    mainSection = models.PositiveSmallIntegerField(
        verbose_name='я хз, что это',
        blank=True,
        null=True,
    )
    country = models.CharField(
        verbose_name='Страна',
        max_length=42,
        blank=True,
        null=True,
    )
    city = models.CharField(
        verbose_name='Город',
        max_length=42,
        blank=True,
        null=True,
    )
    activity = models.CharField(
        verbose_name='Активность (что бы это не значило)',
        max_length=42,
        blank=True,
        null=True,
    )
    status = models.CharField(
        verbose_name='Статус (что бы это не значило)',
        max_length=73,
        blank=True,
        null=True,
    )
    description = models.TextField(
        verbose_name='Здесь должно быть описание группы.',
        blank=True,
        null=True,
    )
    ageLimits = models.PositiveSmallIntegerField(
        verbose_name='Возрастное ограничение (вероятно)',
        blank=True,
        null=True,
    )
    membersCount = models.PositiveIntegerField(
        verbose_name='Количество участников',
        blank=True,
        null=True,
    )
    fixedPost = models.PositiveIntegerField(
        verbose_name='Закреплённый пост',
        blank=True,
        null=True,
    )
    contacts = models.TextField(
        verbose_name='Контакты',
        blank=True,
        null=True,
    )
    site = models.URLField(
        verbose_name='Сайт',
        blank=True,
        null=True,
    )
    isTrending = models.BooleanField(
        verbose_name='В тренде?',
        default=False,
    )
    isVerified = models.BooleanField(
        verbose_name='Подтверждён?',
        default=False,
    )
    hasMarket = models.BooleanField(
        verbose_name='Имеет магазин?',
        default=False,
    )

    def __str__(self):
        return self.name
