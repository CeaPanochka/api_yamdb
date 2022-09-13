import datetime

from django.db import models

from users.models import User

SCORE_CHOICES = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
    (8, 8),
    (9, 9),
    (10, 10),
)


class Genre(models.Model):
    name = models.CharField('Жанр', max_length=256)
    slug = models.SlugField(
        'Ссылка на жанр', max_length=50, unique=True)

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.slug


class Category(models.Model):
    name = models.CharField('Категория', max_length=256)
    slug = models.SlugField(
        'Ссылка на категорию', max_length=50, unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.TextField('Название')
    year = models.PositiveSmallIntegerField('Год выпуска')
    description = models.TextField(
        'Описание', null=True, blank=True)
    genre = models.ManyToManyField(
        Genre, through='GenreTitle',
        related_name='titles',
        verbose_name='Жанр')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='titles',
        verbose_name='Категория')

    class Meta:
        ordering = ('year',)
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"
        constraints = [
            models.CheckConstraint(
                check=models.Q(year__lte=datetime.datetime.now().year),
                name='year_lte_current_year',
            ),
        ]

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE)
    genre = models.ForeignKey(
        Genre,
        verbose_name='Жанр',
        on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Title and genre'
        verbose_name_plural = 'Titles and genres'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва',
    )
    text = models.TextField(
        verbose_name='Текст отзыва',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата добавления отзыва',
        auto_now_add=True,
        db_index=True,
    )
    score = models.IntegerField(
        verbose_name='Оценка',
        choices=SCORE_CHOICES,
    )

    class Meta:
        verbose_name = 'review'
        verbose_name_plural = 'reviews'


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )
    text = models.TextField(
        verbose_name='Текст комментария',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата добавления комментария',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = 'comments'
