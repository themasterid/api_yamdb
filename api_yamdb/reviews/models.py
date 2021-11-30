from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


class Genre(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


class Title(models.Model):
    name = models.CharField(max_length=30)
    year = models.IntegerField(default='Unknown')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Категория'
    )

    def __str__(self):
        return self.title


class Review(models.Model):
    pass


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    review_id = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    def __str__(self):
        return self.text

# class Post(models.Model):
#     text = models.TextField()
#     pub_date = models.DateTimeField(
#         'Дата публикации',
#         auto_now_add=True
#     )
#     author = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='posts',
#     )
#     group = models.ForeignKey(
#         Group,
#         on_delete=models.SET_NULL,
#         blank=True,
#         null=True,
#         related_name='posts',
#     )

#     def __str__(self):
#         return self.text


# class Follow(models.Model):
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='follower',
#         verbose_name='Подписчик',
#     )
#     following = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='following',
#         verbose_name='Подписан',
#     )

#     class Meta:
#         constraints = (
#             models.UniqueConstraint(
#                 fields=('user', 'following'),
#                 name='unique_follow'
#             ),
#         )
