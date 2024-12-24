from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    slug = models.SlugField(unique=True, max_length=50, verbose_name='Слаг')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    slug = models.SlugField(unique=True, max_length=50, verbose_name='Слаг')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    year = models.IntegerField(verbose_name='Год', null=True, blank=True)
    description = models.Charfield(
        verbose_name='Описание', null=True, blank=True
    )
    genre = models.ForeignKey(
        Genres, on_delete=models.SET_NULL, blank=True,
        verbose_name='Жанр', related_name='titles'
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, blank=True,
        null=True, verbose_name='Категория', related_name='titles'
    )
    # rating = ??? непонятно в "redoc" насчет этого поля

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name
        
