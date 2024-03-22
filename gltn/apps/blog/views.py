from django.shortcuts import render
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from ultis.api_helper import api_decorator
from .models import Blog, Image, Like, Comment
from .serializers import BlogSerializer, ImageSerializer, ImageCreateSerializer, GetBlogSerializer, LikeSerializer, \
    CommentSerializer


# Create your views here.
class BlogCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    @api_decorator
    def post(self, request):
        content = request.data.get('content')

        blog = Blog.objects.create(content=content, user=request.user)
        blog.save()
        list_Image = request.data.getlist('images')
        data = [{'avatar': image, 'blog': blog.id} for image in list_Image]
        serializer = ImageCreateSerializer(data=data, many=True, context={'request': request})

        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return BlogSerializer(blog,
                              context={'request': request}).data, 'Create blog successful!', status.HTTP_201_CREATED


class BlogsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @api_decorator
    def get(self, request):
        queryset = Blog.objects.filter(user=request.user, is_active=True).order_by('-created_at')

        data = GetBlogSerializer(queryset, many=True, context={'request': request}).data
        return data, 'Retrieve data successfully!', status.HTTP_200_OK


class BlogAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @api_decorator
    def get(self, request, pk):
        blog = Blog.objects.get(id=pk)
        data = GetBlogSerializer(blog, context={'request': request}).data
        return data, 'Retrieve data successfully!', status.HTTP_200_OK


class BlogUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @api_decorator
    def put(self, request, pk):
        blog = Blog.objects.get(id=pk, user=request.user)

        # update content
        content = request.data.get('content')
        blog.content = content
        blog.save()

        # xóa những ảnh không có trong list id
        id_images = request.data.get('id_images').split(',')
        images = Image.objects.filter(blog=blog)
        for image in images:
            is_del = True
            for id_image in id_images:
                if image.id == id_image:
                    is_del = False
                    break
            if is_del:
                image.delete()

        # lưu ảnh mới của blog được gửi lên
        list_image = request.data.getlist('images')
        data = [{'avatar': image, 'blog': blog.id} for image in list_image]

        serializer = ImageCreateSerializer(data=data, many=True, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return_data = GetBlogSerializer(blog, context={'request': request}).data
        return return_data, 'Update Blog Successful!', status.HTTP_200_OK


class BlogDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @api_decorator
    def delete(self, request, pk):
        blog = Blog.objects.get(id=pk, user=request.user)
        # images = Image.objects.filter(blog=blog)
        # likes = Like.objects.filter(blog=blog)
        # comment = Comment.objects.filter(blog=blog)
        blog.delete()
        # images.delete()
        # likes.delete()
        # comment.delete()
        return {}, 'Delete Blog Successful!', status.HTTP_204_NO_CONTENT


class LikeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @api_decorator
    def post(self, request, pk):

        blog = Blog.objects.get(id=pk)
        check_like = Like.objects.filter(blog=blog, user=request.user)
        if not check_like:
            like = Like.objects.create(blog=blog, user=request.user)

            serializer = LikeSerializer(like, context={'request': request})
            blog.count_like += 1
            blog.save()

            return serializer.data, 'Like successful!', status.HTTP_201_CREATED
        else:
            return {}, 'You has been Liked!', status.HTTP_400_BAD_REQUEST

    @api_decorator
    def delete(self, request, pk):
        blog = Blog.objects.get(id=pk)
        try:

            like = Like.objects.get(blog=blog, user=request.user)
            like.delete()
            blog.count_like -= 1
            blog.save()

            return {}, 'Unlike successful!', status.HTTP_204_NO_CONTENT
        except Exception as e:
            print(e)
            return {}, 'You do not like yet!', status.HTTP_400_BAD_REQUEST


class CountLikeAPIView(APIView):

    @api_decorator
    def get(self, request, pk):
        blog = Blog.objects.get(id=pk)

        return blog.count_like, 'Count successful!', status.HTTP_200_OK


class CommentAPIView(APIView):

    @api_decorator
    def get(self, request):
        blog_id = request.query_params.get('blog_id')
        queryset = Comment.objects.filter().order_by('-created_at')
        if blog_id:
            queryset = queryset.filter(blog_id=blog_id)
        serializer = CommentSerializer(queryset, many=True, context={'request': request})
        return serializer.data, 'Retrieve data successfully!', status.HTTP_200_OK


class CommentInfoAPIView(APIView):

    @api_decorator
    def get(self, request, pk):
        comment = Comment.objects.get(id=pk)
        serializer = CommentSerializer(comment, context={'request': request})
        return serializer.data, 'Retrieve data successfully!', status.HTTP_200_OK


class CreateCommentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @api_decorator
    def post(self, request):
        content = request.data.get('content')
        blog_id = request.data.get('blog_id')

        comment = Comment.objects.create(user=request.user, blog_id=blog_id, content=content)
        serializer = CommentSerializer(comment, context={'request': request})

        return serializer.data, 'Create comment successful!', status.HTTP_201_CREATED


class UpdateCommentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @api_decorator
    def put(self, request, pk):
        content = request.data.get('content')

        comment = Comment.objects.get(id=pk, user=request.user)
        comment.content = content
        comment.save()

        serializer = CommentSerializer(comment, context={'request': request})
        return serializer.data, 'Create comment successful!', status.HTTP_201_CREATED


class DelCommentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @api_decorator
    def delete(self, request, pk):
        try:
            comment = Comment.objects.get(id=pk, user=request.user)
            comment.delete()
            return {}, 'Delete comment successful!', status.HTTP_204_NO_CONTENT
        except Exception as e:
            print(e)
            return {}, 'That is not you comment!', status.HTTP_400_BAD_REQUEST

