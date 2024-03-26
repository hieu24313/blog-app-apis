from django.urls import path
from .views import (BlogCreateAPIView, BlogsAPIView, BlogAPIView, BlogUpdateAPIView, BlogDeleteAPIView, LikeAPIView,
                    CountLikeAPIView, CommentAPIView, CommentInfoAPIView, CreateCommentAPIView, DelCommentAPIView,
                    UpdateCommentAPIView, AddImgBlogAPIView, LikeCommentCreateAPIView, UnLikeCommentAPIView,
                    ReplyCommentAPIView, CreateReplyCommentAPIView, DeleteReplyCommentAPIView,
                    UpdateReplyCommentAPIView, UploadFileAPIView, AddImgForBlog, GetImgUser, HistoryBlogAPIView,
                    HistoryLikeAPIView)

urlpatterns = [
    path('create/', BlogCreateAPIView.as_view()),
    path('blogs/', BlogsAPIView.as_view()),
    path('<uuid:pk>/', BlogAPIView.as_view()),
    path('update/<uuid:pk>/', BlogUpdateAPIView.as_view()),
    path('delete/<uuid:pk>/', BlogDeleteAPIView.as_view()),
    path('image/add/<uuid:pk>/', AddImgBlogAPIView.as_view()),# add ảnh mới
    path('add/images/<uuid:pk>/', AddImgForBlog.as_view()),# add ảnh có sẵn trên server
    path('history/', HistoryBlogAPIView.as_view()),

    path('like/<uuid:pk>/', LikeAPIView.as_view()),
    path('like/count/<uuid:pk>/', CountLikeAPIView.as_view()),
    path('like/history/', HistoryLikeAPIView.as_view()),

    path('comments/', CommentAPIView.as_view()),
    path('comment/<uuid:pk>/', CommentInfoAPIView.as_view()),
    path('comment/create/', CreateCommentAPIView.as_view()),
    path('comment/update/<uuid:pk>/', UpdateCommentAPIView.as_view()),
    path('comment/delete/<uuid:pk>/', DelCommentAPIView.as_view()),

    path('comment/like/<uuid:pk>/', LikeCommentCreateAPIView.as_view()),
    path('comment/unlike/<uuid:pk>/', UnLikeCommentAPIView.as_view()),

    path('file/', UploadFileAPIView.as_view()),
    path('all/image/', GetImgUser.as_view()),

    # --------------------chưa test-----------------
    path('reply/comment/', ReplyCommentAPIView.as_view()),
    path('reply/comment/create/', CreateReplyCommentAPIView.as_view()),
    path('reply/comment/delete/<uuid:pk>/', DeleteReplyCommentAPIView.as_view()),
    path('reply/comment/update/<uuid:pk>/', UpdateReplyCommentAPIView.as_view()),


]
