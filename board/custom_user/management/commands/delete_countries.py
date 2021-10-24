from django.core.management import BaseCommand

from custom_user.models import Country


class Command(BaseCommand):
    help = 'Удаляем все страны из БД'

    def handle(self, *args, **options):
        Country.objects.all().delete()
        print('Все страны успешно удалены')