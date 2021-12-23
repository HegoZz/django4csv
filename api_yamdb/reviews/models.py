from datetime import datetime
import secrets

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


ROLE_CHOICES = (
    ('admin', 'Администратор'),
    ('user', 'Аутентифицированный пользователь'),
    ('moderator', 'Модератор'),
)


def generate_confirmation_code():
    return secrets.token_hex(15)


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


class User(AbstractUser):
    """Кастомизация модели пользователя."""
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль',
        max_length=50,
        choices=ROLE_CHOICES,
        default='user'
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=30,
        default=generate_confirmation_code()
    )
    email = models.EmailField(
        max_length=100,
        unique=True,
    )


class Category(models.Model):
    """Описание модели категории."""
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    name = models.CharField(
        verbose_name='Название категории',
        max_length=256,
    )
    slug = models.SlugField(
        verbose_name='Уникальный идентификатор категории',
        max_length=50,
        unique=True,
    )


class Genre(models.Model):
    """Описание модели жанра."""
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    name = models.CharField(
        verbose_name='Название жанра',
        max_length=256,
    )
    slug = models.SlugField(
        verbose_name='Уникальный идентификатор жанра',
        max_length=50,
        unique=True,
    )


class Title(models.Model):
    """Описание модели произведения."""
    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    name = models.CharField(
        verbose_name='Название произведения',
        max_length=256,
    )
    year = models.SmallIntegerField(
        verbose_name='Год выпуска',
        validators=[validate_year],
    )
    rating = models.SmallIntegerField(
        verbose_name='Рейтинг',
        blank=True,
        null=True,
    )
    description = models.TextField(verbose_name='Описание', blank=True,)
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        verbose_name='Жанр произведения',
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.DO_NOTHING,
    )


class GenreTitle(models.Model):
    """Принадлежность произведения конкретному жанру."""
    title_id = models.ForeignKey(
        Title,
        verbose_name='Произведения',
        on_delete=models.CASCADE,
    )
    genre_id = models.ForeignKey(
        Genre,
        verbose_name='Жанры',
        on_delete=models.DO_NOTHING,
        related_name="titles",
    )


class Review(models.Model):
    """Модель для отзывов."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.SmallIntegerField(validators=[validate_score])
    pub_date = models.DateTimeField(
        default=timezone.now()
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author'
            )
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Модель для комментариев к отзыву."""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        default=timezone.now()
    )

    def __str__(self):
        return self.text
