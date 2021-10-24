from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

CustomUser = get_user_model()


class EmailAndLoginAuthBackend(ModelBackend):
    """
    Аутентификация по логину, либо емейлу.
    Нужно покрыть тестами!!!!
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
            return None

        except CustomUser.MultipleObjectsReturned:
            # В случае, если каким то образом получили 2 юзеров
            return None
        except CustomUser.DoesNotExist:
            # Если юзер на найден
            return None
