from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .manager import CustomUserManager
from .validators.username_validator import custom_username_validator


class CustomUser(AbstractUser):
    """
    Расширение встроенной модели юзера.
    Обязательные поля: email, username, password.
    """

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'), max_length=150, unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator, custom_username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(verbose_name='Емейл адресс', unique=True,
                              error_messages={
                                  'unique': 'Пользователь с данным емейлом уже существует'
                              })
    country = models.ForeignKey('Country', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Страна')
    phone = models.CharField(max_length=11, verbose_name='Номер телефона',
                             null=True, blank=True)
    is_blocked = models.BooleanField('Заблокировать пользователя', default=False)
    subscribers = models.ManyToManyField('self', related_name='subscriptions', symmetrical=False, blank=True)
    posts = models.IntegerField(default=0)
    commentaries = models.IntegerField(default=0)



    objects = CustomUserManager()



    class Meta:
        verbose_name = 'Пользователя'
        verbose_name_plural = 'Пользователи'

    def clean(self):
        self.email = self.email.lower()
        super(CustomUser, self).clean()

    def get_posts(self):
        return self.posts

    def get_comments(self):
        return self.comments

    def __str__(self):
        return self.username


class Country(models.Model):
    """
    Модель страны: Название - флаг
    Поле picture временно может быть пустым`
    """
    name = models.CharField(verbose_name='Страна', max_length=55, unique=True)
    picture = models.ImageField(verbose_name='Флаг', blank=True, null=True, upload_to='countries')

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'
        ordering = ['id']

    def __str__(self):
        return self.name


class IgnoreUser(models.Model):
    """
    Конкретный пользователь может игнорировать любого пользователя
    """
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='user',
        db_index=True
    )
    ignored_user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='ignore_user'
    )
    ignore = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'пользователя в игнор'
        verbose_name_plural = 'Игнорированные пользователи'
        unique_together = ('user', 'ignored_user')

    def __str__(self):
        return 'Пользователь {} игнорирует пользователя {}'.format(
            self.user.username, self.ignored_user.username
        )

    def save(self, *args, **kwargs):
        """
        Проверяем поле ignore перед записью,
        если False, то удаляем запись.
        В противном случае сохраняем, предварительно создав экземпляр
        без этого ошибка - "Cannot force both insert and updating in model saving."
        """
        ignore = self.ignore
        if not ignore:
            self.delete()
        else:
            IgnoreUser(user=self.user, ignored_user=self.ignored_user, ignore=ignore)
            super(IgnoreUser, self).save(*args, **kwargs)
