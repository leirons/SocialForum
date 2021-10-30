from rest_framework.response import Response
from rest_framework.views import APIView
from mysite.models import Theme,Post
from mysite.api.serializers import ThemeSerializer,ThemeDetailSerializer,\
    AddCommentsSerializer,GetPopularityOfPostsSerializer,CreatePostSerializator


class ThemeSerializerv(APIView):
    """Вывод тем"""
    def get(self,request) -> Response:
        themes = Theme.objects.all()
        serializer = ThemeSerializer(themes,many=True)
        return Response(serializer.data)


class ThemeDetailSerializerv(APIView):
    """Вывод одной темы"""
    def get(self,request,pk) -> Response:
        theme = Theme.objects.get(pk=pk)
        serializer = ThemeDetailSerializer(theme)
        return Response(serializer.data)

class CommentsCreate(APIView):
    def post(self,request) -> Response:
        comment = AddCommentsSerializer(data=request.data)
        if comment.is_valid():
            comment.save()
        return Response(status=201)


class GetPopularityPosts(APIView):

    def get(self,request,pk) -> Response:
        post = Post.objects.get(pk=pk)
        serializer = GetPopularityOfPostsSerializer(post)
        return Response(serializer.data)


class CreatePost(APIView)\
        :
    def post(self,request) ->Response:
        post = CreatePostSerializator(data=request.data)
        if post.is_valid():
            post.save()
            return Response(status=201)
        return Response(status=400)

class CreateLike(APIView):
    pass