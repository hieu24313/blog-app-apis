from django.urls import path
from .views import (BlogCreateAPIView, BlogsAPIView, BlogAPIView, BlogUpdateAPIView, BlogDeleteAPIView, LikeAPIView,
                    CountLikeAPIView, CommentAPIView)

urlpatterns = [
    path('blog/create/', BlogCreateAPIView.as_view()),
    path('blogs/', BlogsAPIView.as_view()),
    path('blog/<uuid:pk>/', BlogAPIView.as_view()),
    path('blog/update/<uuid:pk>/', BlogUpdateAPIView.as_view()),
    path('blog/delete/<uuid:pk>/', BlogDeleteAPIView.as_view()),

    path('blog/like/<uuid:pk>/', LikeAPIView.as_view()),
    path('blog/like/count/<uuid:pk>/', CountLikeAPIView.as_view()),

    path('blog/comment/', CommentAPIView.as_view()),

]