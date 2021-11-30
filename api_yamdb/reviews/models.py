from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

ROLE_CHOICES = [
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin')
]


def validate_username(value):
    if value == 'me':
        raise ValidationError(
            ('Имя пользователя не может быть "me"'),
            params={'value': value},
        )


def validate_year(value):
    now = datetime.now().year
    if value > now:
        raise ValidationError(
            f'{value} не может быть больше {now}'
        )


class User(AbstractUser):
    username = models.CharField(
        'Логин пользователя',
        validators=(validate_username,),
        max_length=50,
        unique=True
    )
    email = models.EmailField(
        'Электронная почта',
        max_length=150,
        unique=True
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=True
    )
    role = models.CharField(
        'Роль',
        max_length=20,
        choices=ROLE_CHOICES,
        default='user',
        blank=True
    )
    confirmation_code = models.IntegerField(
        default=0
    )

    @property
    def is_user(self):
        return self.role == 'user'

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    class Meta:
        ordering = ('-username', )
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Имя категории'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг категории'
    )

    class Meta:
        ordering = ('-name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Имя жанра'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг жанра'
    )

    class Meta:
        ordering = ('-name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
        db_index=True
    )
    year = models.IntegerField(
        validators=[validate_year],
        default=0,
        verbose_name='Год',
        db_index=True
    )
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        Category,
        related_name='titles',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        blank=True,
        verbose_name='Жанр'
    )

    class Meta:
        ordering = ('-name',)
        verbose_name = 'Заголовок'
        verbose_name_plural = 'Заголовки'

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.CharField(
        max_length=200
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.IntegerField(
        'Оценка',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ],
        error_messages={'validators': 'Оценка от 1 до 10!'},
        blank=False,
        null=False,
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        db_table = 'reviews'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_author_for_title'
            )]
        ordering = ('-score', 'pub_date',)

    def __str__(self):
        return self.text


class Comments(models.Model):
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.CharField(
        'Текст комментария',
        max_length=200
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
