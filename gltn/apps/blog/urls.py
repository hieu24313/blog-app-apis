from django.urls import path
from .views import (BlogCreateAPIView, BlogsAPIView, BlogAPIView, BlogUpdateAPIView, BlogDeleteAPIView, LikeAPIView,
                    CountLikeAPIView, CommentAPIView, CommentInfoAPIView, CreateCommentAPIView, DelCommentAPIView,
                    UpdateCommentAPIView)

urlpatterns = [
    path('blog/create/', BlogCreateAPIView.as_view()),
    path('blogs/', BlogsAPIView.as_view()),
    path('blog/<uuid:pk>/', BlogAPIView.as_view()),
    path('blog/update/<uuid:pk>/', BlogUpdateAPIView.as_view()),
    path('blog/delete/<uuid:pk>/', BlogDeleteAPIView.as_view()),

    path('blog/like/<uuid:pk>/', LikeAPIView.as_view()),
    path('blog/like/count/<uuid:pk>/', CountLikeAPIView.as_view()),

    path('blog/comments/', CommentAPIView.as_view()),
    path('blog/comment/<uuid:pk>/', CommentInfoAPIView.as_view()),
    path('blog/comment/create/', CreateCommentAPIView.as_view()),
    path('blog/comment/update/<uuid:pk>/', UpdateCommentAPIView.as_view()),
    path('blog/comment/delete/<uuid:pk>/', DelCommentAPIView.as_view()),

]
