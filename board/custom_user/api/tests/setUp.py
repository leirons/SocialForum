from django.contrib.auth import get_user_model
from django.test import TestCase

from custom_user.models import Country, IgnoreUser
from mysite.models import (
    Subject, Theme,
    Post, Comments
)

User = get_user_model()


class SetUp(TestCase):

    def setUp(self):
        self.user_1 = User.objects.create(username='BeginnerA234', first_name='Kirill', last_name='Lobashov',
                                          email='proverka@gmail.com', password='proverka3004')
        self.user_2 = User.objects.create(username='User2', first_name='Andrey', last_name='Palchikov',
                                          email='palchikov_andrey@yandex.ru', password='proverka1234')
        self.user_3 = User.objects.create(username='User3', first_name='Vladimir', last_name='Putin',
                                          email='VladimirVladimirovich@mail.ru', password='proverka1234')
        subject = Subject.objects.create(title='Разное')
        theme = Theme.objects.create(title='Таверна', creator=self.user_1, subject=subject, slug='Taverna')
        post = Post.objects.create(user=self.user_1, title='Вброс', text='Random text', where_we_are=theme)
        Comments.objects.create(user=self.user_1, post=post, body='blablabla')
        Comments.objects.create(user=self.user_1, post=post, body='rqwwqr')
        Comments.objects.create(user=self.user_1, post=post, body='dfamfa')
        Comments.objects.create(user=self.user_2, post=post, body='dfamfa')
        Comments.objects.create(user=self.user_3, post=post, body='dfamfa')
        country = Country.objects.create(name='Россия')
        self.user_1.subscribers.add(self.user_2.id, self.user_3.id)
        User.objects.filter(pk=self.user_1.id).update(country=country)
        IgnoreUser(user=self.user_2, ignored_user=self.user_3, ignore=True).save()
        IgnoreUser(user=self.user_2, ignored_user=self.user_1, ignore=True).save()
