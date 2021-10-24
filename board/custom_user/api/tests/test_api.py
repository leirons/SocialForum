import json

from django.contrib.auth import get_user_model
from django.db import connection
from django.db.models import Count
from django.test.utils import CaptureQueriesContext
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from custom_user.api.serializers import UserProfileSerializer
from custom_user.api.tests.setUp import SetUp
from custom_user.models import CustomUser, IgnoreUser

User = get_user_model()


class UserCreateAPITestCase(APITestCase):

    def setUp(self):
        self.url = reverse('register-list')

    def test_response(self):
        get = self.client.get(self.url)
        post = self.client.post(self.url)
        put = self.client.get(self.url)
        delete = self.client.delete(self.url)
        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, get.status_code)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, post.status_code)
        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, put.status_code)
        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, delete.status_code)

    def test_create(self):
        before = User.objects.count()
        data = {
            'username': 'admin',
            'email': 'admin@admin.com',
            'password': 'useruser',
            'password2': 'useruser'
        }
        json_data = json.dumps(data)
        response = self.client.post(self.url, data=json_data, content_type='application/json')
        after = User.objects.count()
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(0, before)
        self.assertEqual(1, after)

    def test_not_valid_username(self):
        before = User.objects.count()
        data = {
            'username': 'admin@gmail.com',
            'email': 'admin@admin.com',
            'password': 'useruser',
            'password2': 'useruser'
        }
        json_data = json.dumps(data)
        response = self.client.post(self.url, data=json_data, content_type='application/json')
        after = User.objects.count()
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(0, before)
        self.assertEqual(0, after)

    def test_not_valid_email(self):
        before = User.objects.count()
        data = {
            'username': 'admin',
            'email': 'admin@admin',
            'password': 'useruser',
            'password2': 'useruser'
        }
        json_data = json.dumps(data)
        response = self.client.post(self.url, data=json_data, content_type='application/json')
        after = User.objects.count()
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(0, before)
        self.assertEqual(0, after)

    def test_unique_email(self):
        before = User.objects.count()
        user1_data = {
            'username': 'admin',
            'email': 'admin@admin.ru',
            'password': 'useruser',
            'password2': 'useruser'
        }

        json_data = json.dumps(user1_data)
        response_user1 = self.client.post(self.url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response_user1.status_code)
        user2_data = {
            'username': 'admin1',
            'email': 'ADMIN@admin.ru',
            'password': 'useruser',
            'password2': 'useruser'
        }
        json_data = json.dumps(user2_data)
        response_user2 = self.client.post(self.url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response_user2.status_code)
        after = User.objects.count()
        self.assertEqual(0, before)
        self.assertEqual(1, after)


class ProfileAPITestCase(APITestCase, SetUp):

    def test_response(self):
        url = reverse('profile-detail', args=(self.user_1.username,))
        get = self.client.get(url)
        post = self.client.post(url)
        put = self.client.get(url)
        delete = self.client.delete(url)
        self.assertEqual(status.HTTP_200_OK, get.status_code)
        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, post.status_code)
        self.assertEqual(status.HTTP_200_OK, put.status_code)
        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, delete.status_code)

    def test_queries(self):
        url = reverse('profile-detail', args=(self.user_1.username,))
        with CaptureQueriesContext(connection) as queries:
            self.client.get(url)
            self.assertEqual(4, len(queries))

    def test_get_detail(self):
        url = reverse('profile-detail', args=(self.user_1.username,))
        response = self.client.get(url)
        queryset = User.objects.all().annotate(
            subscribers_count=Count('subscribers'),
        ).select_related('country').prefetch_related('subscribers', 'comments_set', 'user').order_by('id').first()
        serializer_data = UserProfileSerializer(queryset).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_patch_is_owner(self):
        url = reverse('profile-detail', args=(self.user_1.username,))
        self.client.force_login(self.user_1)
        data = {
            'username': 'krabik',
        }
        json_data = json.dumps(data)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.user_1.refresh_from_db()
        self.assertEqual('krabik', self.user_1.username)

    def test_patch_not_owner_but_staff(self):
        staff = CustomUser.objects.create(username='STAFF', email='staf@staf.staf',
                                          password='useruser', is_staff=True)
        url = reverse('profile-detail', args=(self.user_1.username,))
        self.client.force_login(staff)
        data = {
            'username': 'krabik',
        }
        json_data = json.dumps(data)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.user_1.refresh_from_db()
        self.assertEqual('krabik', self.user_1.username)

    def test_patch_is_not_owner(self):
        url = reverse('profile-detail', args=(self.user_1.username,))
        self.client.force_login(self.user_2)
        data = {
            'username': 'krabik',
        }
        json_data = json.dumps(data)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.user_1.refresh_from_db()
        self.assertEqual('BeginnerA234', self.user_1.username)


class IgnoreUserTestCase(APITestCase):

    def setUp(self):
        self.user_1 = User.objects.create(username='BeginnerA234', first_name='Kirill', last_name='Lobashov',
                                          email='proverka@gmail.com', password='proverka3004', is_active=True)
        self.user_2 = User.objects.create(username='User2', first_name='Andrey', last_name='Palchikov',
                                          email='palchikov_andrey@yandex.ru', password='proverka1234')
        self.user_3 = User.objects.create(username='User3', first_name='Vladimir', last_name='Putin',
                                          email='VladimirVladimirovich@mail.ru', password='proverka1234')

    def test_is_active_user_ignore_user(self):
        url = reverse('ignore-user-list')
        self.client.force_login(self.user_1)
        before = IgnoreUser.objects.filter(user=self.user_1).count()
        self.assertEqual(0, before)
        data = {
            'user': self.user_1.id,
            'ignored_user': self.user_2.id,
            'ignore': True
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        after = IgnoreUser.objects.filter(user=self.user_1).count()
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(1, after)

    def test_put_ignore_user_is_owner(self):
        url = reverse('ignore-user-list')
        self.client.force_login(self.user_1)
        before = IgnoreUser.objects.filter(user=self.user_1).count()
        self.assertEqual(0, before)
        data = {
            'user': self.user_1.id,
            'ignored_user': self.user_2.id,
            'ignore': True
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        after = IgnoreUser.objects.filter(user=self.user_1).count()
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(1, after)
        id = self.user_1.user.all().first().id
        url_detail = reverse('ignore-user-detail', args=(id,))
        data = {
            'user': self.user_1.id,
            'ignored_user': self.user_2.id,
            'ignore': False
        }
        json_data = json.dumps(data)
        response = self.client.put(url_detail, data=json_data, content_type='application/json')
        after = IgnoreUser.objects.filter(user=self.user_1).count()
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(0, after)

    def test_put_ignore_user_not_owner(self):
        url = reverse('ignore-user-list')
        self.client.force_login(self.user_1)
        before = IgnoreUser.objects.filter(user=self.user_1).count()
        self.assertEqual(0, before)
        data = {
            'user': self.user_1.id,
            'ignored_user': self.user_2.id,
            'ignore': True
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        after = IgnoreUser.objects.filter(user=self.user_1).count()
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(1, after)
        self.client.logout()
        self.client.force_login(self.user_2)
        id = self.user_1.user.all().first().id
        url_detail = reverse('ignore-user-detail', args=(id,))
        data = {
            'user': self.user_1.id,
            'ignored_user': self.user_2.id,
            'ignore': False
        }
        json_data = json.dumps(data)
        response = self.client.put(url_detail, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_put_ignore_user_not_owner_is_superuser(self):
        superuser = User.objects.create(username='superuser', first_name='Kirill', last_name='Lobashov',
                                        email='abrakadabra@gmail.com', password='proverka3004', is_active=True,
                                        is_superuser=True)
        url = reverse('ignore-user-list')
        self.client.force_login(self.user_1)
        before = IgnoreUser.objects.filter(user=self.user_1).count()
        self.assertEqual(0, before)
        data = {
            'user': self.user_1.id,
            'ignored_user': self.user_2.id,
            'ignore': True
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        after = IgnoreUser.objects.filter(user=self.user_1).count()
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(1, after)
        self.client.logout()
        self.client.force_login(superuser)
        id = self.user_1.user.all().first().id
        url_detail = reverse('ignore-user-detail', args=(id,))
        data = {
            'user': self.user_1.id,
            'ignored_user': self.user_2.id,
            'ignore': False
        }
        json_data = json.dumps(data)
        response = self.client.put(url_detail, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_put_ignore_user_not_owner_is_anonym(self):
        url = reverse('ignore-user-list')
        self.client.force_login(self.user_1)
        before = IgnoreUser.objects.filter(user=self.user_1).count()
        self.assertEqual(0, before)
        data = {
            'user': self.user_1.id,
            'ignored_user': self.user_2.id,
            'ignore': True
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        after = IgnoreUser.objects.filter(user=self.user_1).count()
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(1, after)
        self.client.logout()
        # anonym put
        id = self.user_1.user.all().first().id
        url_detail = reverse('ignore-user-detail', args=(id,))
        data = {
            'user': self.user_1.id,
            'ignored_user': self.user_2.id,
            'ignore': False
        }
        json_data = json.dumps(data)
        response = self.client.put(url_detail, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_unique_ignore_user(self):
        url = reverse('ignore-user-list')
        self.client.force_login(self.user_1)
        before = IgnoreUser.objects.filter(user=self.user_1).count()
        self.assertEqual(0, before)
        data = {
            'user': self.user_1.id,
            'ignored_user': self.user_2.id,
            'ignore': True
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.client.post(url, data=json_data, content_type='application/json')
        self.client.post(url, data=json_data, content_type='application/json')
        self.client.post(url, data=json_data, content_type='application/json')
        after = IgnoreUser.objects.filter(user=self.user_1).count()
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(1, after)
        data = {
            'user': self.user_1.id,
            'ignored_user': self.user_2.id,
            'ignore': False
        }
        json_data = json.dumps(data)
        id = self.user_1.user.all().first().id
        url_detail = reverse('ignore-user-detail', args=(id,))
        response = self.client.put(url_detail, data=json_data, content_type='application/json')
        after = IgnoreUser.objects.filter(user=self.user_1).count()
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(0, after)

    def test_unique_many_ignore_user(self):
        url = reverse('ignore-user-list')
        self.client.force_login(self.user_1)
        before = IgnoreUser.objects.filter(user=self.user_1).count()
        self.assertEqual(0, before)
        data = {
            'user': self.user_1.id,
            'ignored_user': self.user_2.id,
            'ignore': True
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        after = IgnoreUser.objects.filter(user=self.user_1).count()
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(1, after)
        self.client.force_login(self.user_2)
        before = IgnoreUser.objects.filter(user=self.user_2).count()
        self.assertEqual(0, before)
        data = {
            'user': self.user_2.id,
            'ignored_user': self.user_1.id,
            'ignore': True
        }

        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        data = {
            'user': self.user_2.id,
            'ignored_user': self.user_3.id,
            'ignore': True
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        after = IgnoreUser.objects.filter(user=self.user_2).count()
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(2, after)
        data = {
            'user': self.user_2.id,
            'ignored_user': self.user_1.id,
            'ignore': False
        }
        json_data = json.dumps(data)
        id = self.user_2.user.all().first().id
        url_detail = reverse('ignore-user-detail', args=(id,))
        response = self.client.put(url_detail, data=json_data, content_type='application/json')
        after = IgnoreUser.objects.filter(user=self.user_2).count()
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(1, after)

    def test_attacker_wants_second_user_ignore_third_user(self):
        url = reverse('ignore-user-list')
        self.client.force_login(self.user_1)
        before = IgnoreUser.objects.filter(user=self.user_2).count()
        self.assertEqual(0, before)
        data = {
            'user': self.user_2.id,
            'ignored_user': self.user_3.id,
            'ignore': True
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        after = IgnoreUser.objects.filter(user=self.user_2).count()
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(0, after)

    def test_anonym_wants_second_user_ignore_third_user(self):
        url = reverse('ignore-user-list')
        before = IgnoreUser.objects.filter(user=self.user_2).count()
        self.assertEqual(0, before)
        data = {
            'user': self.user_2.id,
            'ignored_user': self.user_3.id,
            'ignore': True
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        after = IgnoreUser.objects.filter(user=self.user_2).count()
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertEqual(0, after)

    def test_superuser_wants_second_user_ignore_third_user(self):
        superuser = User.objects.create(username='superuser', first_name='Kirill', last_name='Lobashov',
                                        email='abrakadabra@gmail.com', password='proverka3004', is_active=True,
                                        is_superuser=True)
        url = reverse('ignore-user-list')
        self.client.force_login(superuser)
        before = IgnoreUser.objects.filter(user=self.user_2).count()
        self.assertEqual(0, before)
        data = {
            'user': self.user_2.id,
            'ignored_user': self.user_3.id,
            'ignore': True
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        after = IgnoreUser.objects.filter(user=self.user_2).count()
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(0, after)
