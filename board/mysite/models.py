from django.db import models
from django.urls import reverse

from board import settings

from custom_user.models import CustomUser

from .utils.bad_words import change_all_bad_words


class Subject(models.Model):
    """Обьект обсуждения, он может быть только 1"""

    title = models.CharField(max_length=50, verbose_name="Название", )

    class Meta:
        ordering = ['title']
        verbose_name_plural = 'Обьекы обсуждения'
        verbose_name = 'Обьект обсуждения'

    def __str__(self):
        return self.title


class Theme(models.Model):
    """Темы для обсуждения, внутри обьекта обсуждения"""

    title = models.CharField(max_length=50, verbose_name="Название")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='creator',
                                verbose_name='Пользователь создавший тему')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='subject',
                                verbose_name='Тема обсуждения')
    slug = models.SlugField(null=True, verbose_name='ссылка на страницу')

    class Meta:
        ordering = ['title']
        verbose_name_plural = 'Темы'
        verbose_name = 'Тема'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'slug': self.slug})


class Post(models.Model):
    """Посты в темах для обсуждения, пост может создавать только зареганный юзер"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=50, verbose_name="Название")
    text = models.TextField(max_length=500, verbose_name="Текст")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    where_we_are = models.ForeignKey(Theme, on_delete=models.CASCADE, related_name='get_news', null=True, blank=True)
    popularity = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)

    class Meta:
        ordering = ['created_at']
        verbose_name_plural = 'Посты'
        verbose_name = 'Пост'

    def __str__(self):
        return self.title


class Comments(models.Model):
    """Комментарии в постах для обсуждения"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='posts')
    body = models.TextField(max_length=500)
    created_on = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return f'Пользователь {self.post}'

    class Meta:
        ordering = ['created_on']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def clean(self):
        self.body = change_all_bad_words(self.body)
        super(Comments, self).clean()
