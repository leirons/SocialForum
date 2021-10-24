from django.db.models.signals import pre_save
from django.dispatch import receiver

from board import settings
from custom_user.validators.username_validator import custom_username_validator

User = settings.AUTH_USER_MODEL



@receiver(signal=pre_save, sender=User)
def validate_username_field(sender, instance, *args, **kwargs):
    """
    Валидируем username перед сохранением в базу
    """
    custom_username_validator(instance.username)
