from django.db.models import Count
from rest_framework import mixins

from rest_framework.viewsets import GenericViewSet, ModelViewSet

from rest_framework.permissions import IsAdminUser
from custom_user.api.permissions import (
    IsOwnerOrStaffOrReadOnly,
    IsAuthenticateAndIsOwner
)
from custom_user.api.serializers import UserProfileSerializer, IgnoreUserSerializer, UserRegisterSerializer, \
    CountrySerializer
from custom_user.models import CustomUser, IgnoreUser, Country


class UserRegisterView(mixins.CreateModelMixin,
                       GenericViewSet):
    serializer_class = UserRegisterSerializer
    queryset = CustomUser.objects.all()


class UserProfileRetrieveView(mixins.RetrieveModelMixin,
                              mixins.UpdateModelMixin,
                              GenericViewSet):
    """Вью профиля, с личной информацией и статистикой"""

    serializer_class = UserProfileSerializer
    permission_classes = [IsOwnerOrStaffOrReadOnly, ]
    queryset = CustomUser.objects.all().annotate(
        subscribers_count=Count('subscribers'),
    ).select_related('country').prefetch_related('subscribers', 'comments_set', 'user').order_by('id')
    lookup_field = 'username'


class IgnoreUserViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    serializer_class = IgnoreUserSerializer
    queryset = IgnoreUser.objects.all()
    permission_classes = [IsAuthenticateAndIsOwner, ]


class CountryCreateView(mixins.CreateModelMixin,
                        GenericViewSet):
    serializer_class = CountrySerializer
    queryset = Country.objects.all()
    permission_classes = [IsAdminUser, ]
