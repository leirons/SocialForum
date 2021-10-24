import re
from django.core.exceptions import ValidationError


def custom_username_validator(username):
    """
    Исключаем возможность записи емейлов в username
    """
    if re.fullmatch('\\w+@\\w+.\\w+', username):
        raise ValidationError(['Имя пользователя cхож с емейлом.', 'Пожалуйста придумайте другой логин'])


def custom_email_validator(email):
    """
    Проверяем на уникальность емейл в БД.
    """
    from custom_user.models import CustomUser
    if CustomUser.objects.filter(email=email.lower()):
        raise ValidationError('Указанный емейл занят')
