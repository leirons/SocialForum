from django.urls import path

from .views import MultipleModelView, Themes, Posts, \
    EditComments, EditPost, CreateComment, \
    CreatePost,subscribe


urlpatterns = [
    path('', MultipleModelView.as_view(), name='themes'),
    path('<slug:slug>', Themes.as_view(), name='article_detail'),
    path('posts/<int:pk>/', Posts.as_view(), name='posts'),
    path('posts/Edit/<int:pk>/', EditComments.as_view(), name='update_comment'),
    path('post_edit/<int:pk>/', EditPost.as_view(), name='post'),
    path('posts/post_edit/create_comment/', CreateComment.as_view(), name='create_comment'),
    path('posts/post_edit/create_post/<slug:slug>/', CreatePost.as_view(), name='create_post'),
    path('subscription/',subscribe,name='subs'),

]
