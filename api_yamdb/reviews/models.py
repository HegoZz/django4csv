from django.db import models


class Category(models.Model):
    """Описание модели категории."""
    name = models.CharField(verbose_name="Название категории", max_length=256)
    slug = models.SlugField(
        verbose_name="Уникальный идентификатор категории",
        max_length=50,
        unique=True
    )


class Genre(models.Model):
    """Описание модели жанра."""
    name = models.CharField(verbose_name="Название жанра", max_length=256)
    slug = models.SlugField(
        verbose_name="Уникальный идентификатор жанра",
        max_length=50,
        unique=True
    )


class Title(models.Model):
    name = models.CharField(verbose_name="Название жанра", max_length=256)
    year = models.SmallIntegerField(verbose_name="Год выпуска")
    rating = models.SmallIntegerField(verbose_name="Рейтинг",
                                      blank=True, null=True)
    description = models.TextField(verbose_name="Описание", blank=True)
    genre = models.ForeignKey(
        Genre,
        verbose_name='Жанры',
        on_delete=models.DO_NOTHING,
        related_name="titles",
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.DO_NOTHING,
        related_name="titles",
    )
