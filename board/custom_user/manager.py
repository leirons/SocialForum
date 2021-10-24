from django.apps import apps
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager


class CustomUserManager(UserManager):
    """Для возможности будущего расширения"""

    def _create_user(self, username, email, password, **extra_fields):
        """
        Создание и сохранение юзера.
        Теперь обязательные поля для менеджера email и password.
        """

        if not username:
            raise ValueError('The given username must be set')
        if not email:
            raise ValueError('The given email must be set')
        if not password:
            raise ValueError('The given password must be set')
        email = self.normalize_email(email)
        GlobalUserModel = apps.get_model(self.model._meta.app_label, self.model._meta.object_name)
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.clean()
        user.save(using=self._db)
        return user
