from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from custom_user.models import CustomUser, Country, IgnoreUser
from custom_user.validators.username_validator import custom_email_validator


class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[custom_email_validator])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'password',
            'password2',
        )

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                'password': 'Указанные пароли не совпадают'
            })
        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'].lower(),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class CountrySerializer(serializers.ModelSerializer):
    """
    Вспомогательный сериализатор для профиля пользователя.
    Помогает извлечь информацию полей из модели Country
    """

    class Meta:
        model = Country
        fields = (
            'name',
            'picture'
        )


class UserFieldSerializer(serializers.ModelSerializer):
    """
    Вспомогательный сериализатор для профиля пользователя.
    Помогает извлечь информацию полей из модели CustomUser
    """

    class Meta:
        model = CustomUser
        fields = (
            'id',
            'username'
        )


class IgnoreUserSerializer(serializers.ModelSerializer):
    """
    Сериалайзер игнора
    """

    class Meta:
        model = IgnoreUser
        fields = (
            'id',
            'user',
            'ignored_user',
            'ignore'
        )


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Сериалайзер профиля пользователя.
    Выводится статистика и личная информация
    """
    country = CountrySerializer(read_only=True)
    subscribers = UserFieldSerializer(read_only=True, many=True)
    subscribers_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.SerializerMethodField()
    user_ignore_list = IgnoreUserSerializer(many=True, read_only=True, source='user')

    class Meta:
        model = CustomUser
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'phone',
            'is_blocked',
            'comments_count',
            'subscribers',
            'subscribers_count',
            'country',
            'user_ignore_list'
        )

    @staticmethod
    def get_comments_count(instance):
        return instance.comments_set.count()
