from django.urls import path
from .views import *

urlpatterns = [
    path("theme/",ThemeSerializerv.as_view()),
    path("theme/<int:pk>", ThemeDetailSerializerv.as_view()),
    path("comments/", CommentsCreate.as_view()),
    path('get_popularity/<int:pk>',GetPopularityPosts.as_view()),
]