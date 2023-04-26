from django.contrib.auth import get_user_model
from django.db import models
from staj import settings


class Post(models.Model):
    description = models.CharField(verbose_name='Описание', null=False, max_length=200)
    image = models.ImageField(verbose_name='Фото', null=False, blank=True, upload_to='posts')
    author = models.ForeignKey(verbose_name='Автор', to=get_user_model(), related_name='posts', null=False, blank=False,
                               on_delete=models.CASCADE)
    created_at = models.DateTimeField(verbose_name='Дата создания публикации', auto_now_add=True)
    like_count = models.IntegerField(default=0)
    views_count = models.IntegerField(default=0)

class Comment(models.Model):
    author = models.ForeignKey(verbose_name='Автор', to=get_user_model(), related_name='comments', null=False,
                               blank=False,
                               on_delete=models.CASCADE)
    post = models.ForeignKey(verbose_name='Публикация', to='blog.Post', related_name='comments', null=False,
                             blank=False,
                             on_delete=models.CASCADE)
    text = models.CharField(verbose_name='Комментарий', null=False, blank=False, max_length=200)


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

class Favorite(models.Model):
    user = models.ForeignKey(
        to=get_user_model(),
        related_name='favorite_posts',
        verbose_name='Избранное',
        null=False,
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        to=Post,
        related_name='favorite_users',
        verbose_name='Избранное',
        null=False,
        on_delete=models.CASCADE
    )
    note = models.CharField(
        max_length=30,
        verbose_name='Текстовая заметка',
        null=False,
        blank=True
    )

    class Meta:
        verbose_name = 'Избранная запись',
        verbose_name_plural = 'Избранные записи'