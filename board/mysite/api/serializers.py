from rest_framework import serializers
from mysite.models import Theme,Comments,Post
from custom_user.api.serializers import UserFieldSerializer


class ThemeSerializer(serializers.ModelSerializer):
    """Вывод Тем от пользователей"""
    class Meta:
        model = Theme
        fields = ['title','creator','subject']


class ThemeDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Theme
        fields = ['title','slug']


class AddCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['user','post','body','created_on']


class GetPopularityOfPostsSerializer(serializers.ModelSerializer):
    user = UserFieldSerializer(read_only=True)
    where_we_are = ThemeDetailSerializer(read_only=True)
    title = serializers.CharField()
    popularity = serializers.IntegerField()
    class Meta:
        model = Post
        fields = ['user','title','text','where_we_are','popularity']


class CreatePostSerializator(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'text']

class CreateLikeSerializator(serializers.ModelSerializer):
    class Meta:
        model = Comments
        pass