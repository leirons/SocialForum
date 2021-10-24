from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth import get_user_model

from custom_user.models import IgnoreUser


User = get_user_model()


class TestUser(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(username='proverka', email='proverka@gmail.com', password='proverka3004')

    def test_create_user(self):
        user = User.objects.get(username='proverka')
        self.assertEqual(self.user, user)

    def test_is_superuser(self):
        user = User.objects.get(username='proverka')
        self.assertFalse(user.is_superuser)

    def test_is_staff(self):
        user = User.objects.get(username='proverka')
        self.assertFalse(user.is_staff)

    def test_email_is_lower(self):
        user = User.objects.create_user(username='random_user', email='RAndOM@emaIL.CoM', password='proverka3004')
        self.assertEqual(user.email, 'random@email.com')

    def test_email_is_not_email(self):
        try:
            user = User.objects.create_user(username='random_user', password='proverka3004')
            if user:
                self.assertEqual(1, 2)
        except ValueError:
            self.assertEqual(1, 1)

    def test_correct_username(self):
        """
        Тест заработал благодаря тому, что
        добавил валидацую в менеджер
        """
        try:
            # User.objects.model -> full_clean необходимо вызвать
            user = User.objects.create_user(username='asdasd@mail.ru', email='proverka1@gmail.com',
                                            password='proverka3004')
            if user:
                self.assertEqual(1, 2)
        except ValidationError:
            pass


class TestIgnoreList(TestCase):

    def setUp(self) -> None:
        self.user_1 = User.objects.create_user(username='beginner', email='random@mail.ru', password='12345678')
        self.user_2 = User.objects.create_user(username='blabla', email='blabla@gmail.com', password='blablablabla')

    def test_ignoring_user(self):
        ignore_user = IgnoreUser(user=self.user_1, ignored_user=self.user_2, ignore=True)
        ignore_user.save()
        query = IgnoreUser.objects.get(user=self.user_1)
        self.assertEqual(ignore_user, query)
        self.assertEqual(ignore_user.ignore, query.ignore)

    def test_remove_ignore_user(self):
        self.test_ignoring_user()
        ignore_user = IgnoreUser.objects.get(user=self.user_1, ignored_user=self.user_2)
        ignore_user.ignore = False
        ignore_user.save()
        self.assertEqual(0, len(IgnoreUser.objects.filter(user=self.user_1, ignored_user=self.user_2)))
