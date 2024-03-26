from django.shortcuts import render
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ultis.api_helper import api_decorator
from ultis.helper import CustomPagination
from .models import Blog, Image, Like, Comment, ImageComment, LikeComment, ReplyComment, BlogImage, FileUpload
from .serializers import BlogSerializer, ImageCreateSerializer, GetBlogSerializer, LikeSerializer, \
    CommentSerializer, ImageCommentSerializer, LikeCommentSerializer, ReplyCommentSerializer, ImageUploadSerializer, \
    GetImageUploadSerializer, BlogImgSerializer


class BlogCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    # parser_classes = [MultiPartParser]

    @api_decorator
    def post(self, request):
        content = request.data.get('content')

        blog = Blog.objects.create(content=content, user=request.user)
        blog.save()
        list_Image = request.data.get('images').split(',')
        if list_Image:
            data = [{'image': image, 'blog': blog.id} for image in list_Image]
            serializer = BlogImgSerializer(data=data, many=True, context={'request': request})

            if serializer.is_valid(raise_exception=True):
                serializer.save()
        data = BlogSerializer(blog, context={'request': request}).data
        queryset_img = FileUpload.objects.filter(id__in=list_Image)
        serializer_img = GetImageUploadSerializer(queryset_img, many=True, context={'request': request}).data
        data['image'] = serializer_img
        return data, 'Create blog successful!', status.HTTP_201_CREATED


class BlogsAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    @api_decorator
    def get(self, request):
        queryset = Blog.objects.filter().order_by('-created_at')

        data = BlogSerializer(queryset, many=True, context={'request': request}).data
        return data, 'Retrieve data successfully!', status.HTTP_200_OK


class BlogAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    @api_decorator
    def get(self, request, pk):
        blog = Blog.objects.get(id=pk)
        print(blog)
        liked = False
        check_like = Like.objects.filter(blog=blog, user=request.user)
        if check_like:
            liked = True
        data = GetBlogSerializer(blog, context={'request': request}).data
        data['liked'] = liked
        return data, 'Retrieve data successfully!', status.HTTP_200_OK


class AddImgBlogAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @api_decorator
    def post(self, request, pk):
        blog = Blog.objects.get(id=pk)
        list_image = request.data.getlist('images')
        data = [{'avatar': image, 'blog': blog.id} for image in list_image]
        serializer = ImageCreateSerializer(data=data, many=True, context={'request': request})

        if serializer.is_valid(raise_exception=True):
            serializer.save()
        data = BlogSerializer(blog, context={'request': request}).data
        return data, 'Add images successful!', status.HTTP_200_OK


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
        images = BlogImage.objects.filter(blog=blog)
        for image in images:
            is_del = True
            for id_image in id_images:
                if str(id_image) == str(image.image.id):
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
        blog.delete()
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

            return {}, 'Unlike successful!', status.HTTP_200_OK
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
        paginator = CustomPagination()
        paginator.add_total_record(len(queryset))
        result = paginator.paginate_queryset(queryset, request)
        serializer = CommentSerializer(result, many=True, context={'request': request})
        data = paginator.get_paginated_response(serializer.data).data
        return data, 'Retrieve data successfully!', status.HTTP_200_OK


class CommentInfoAPIView(APIView):

    @api_decorator
    def get(self, request, pk):
        comment = Comment.objects.get(id=pk)

        data = CommentSerializer(comment, context={'request': request}).data
        if request.user.is_anonymous:
            pass
        else:
            check = LikeComment.objects.filter(comment=comment, user=request.user)
            data['liked'] = len(check) > 0
        return data, 'Retrieve data successfully!', status.HTTP_200_OK


class CreateCommentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @api_decorator
    def post(self, request):
        content = request.data.get('content')
        blog_id = request.data.get('blog_id')
        comment = Comment.objects.create(user=request.user, blog_id=blog_id, content=content)

        list_Image = request.data.getlist('images')
        if list_Image:
            data = [{'avatar': image, 'comment': comment.id} for image in list_Image]
            serializer = ImageCommentSerializer(data=data, many=True, context={'request': request})

            if serializer.is_valid(raise_exception=True):
                serializer.save()

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

        # xóa những ảnh không có trong list id
        id_images = request.data.get('id_images').split(',')
        images = ImageComment.objects.filter(comment=comment)
        for image in images:
            is_del = True
            for id_image in id_images:
                if str(id_image) == str(image.id):
                    is_del = False
                    break
            if is_del:
                print('xóa')
                image.delete()

        # lưu ảnh mới của blog được gửi lên
        list_image = request.data.getlist('images')
        data = [{'avatar': image, 'comment': comment.id} for image in list_image]

        serializer = ImageCommentSerializer(data=data, many=True, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        serializer = CommentSerializer(comment, context={'request': request})
        return serializer.data, 'Update comment successful!', status.HTTP_200_OK


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
            return {}, 'That is not your comment!', status.HTTP_400_BAD_REQUEST


class LikeCommentCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @api_decorator
    def post(self, request, pk):
        comment = Comment.objects.get(id=pk)
        check = LikeComment.objects.filter(comment=comment, user=request.user)

        if not check:
            like_cmt = LikeComment.objects.create(comment=comment, user=request.user)
            comment.count_like += 1
            comment.save()
            serializer = LikeCommentSerializer(like_cmt, context={'request': request})
            return serializer.data, 'Like successful!', status.HTTP_201_CREATED
        else:
            return {}, 'Liked', status.HTTP_400_BAD_REQUEST


class UnLikeCommentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @api_decorator
    def delete(self, request, pk):
        comment = Comment.objects.get(id=pk)
        comment.count_like -= 1
        comment.save()
        try:
            like_cmt = LikeComment.objects.get(comment=comment, user=request.user)
            like_cmt.delete()
            return {}, 'Unlike successful!', status.HTTP_204_NO_CONTENT
        except Exception as e:
            print(e)
            return {}, 'You do not like yet!', status.HTTP_400_BAD_REQUEST


class ReplyCommentAPIView(APIView):

    @api_decorator
    def get(self, request):
        comment_id = request.query_params.get('comment_id')
        queryset = ReplyComment.objects.filter()

        # if comment_id:
        #     queryset = queryset.filter(comment_id=comment_id)
        serializer = ReplyCommentSerializer(queryset, context={'request': request})
        return serializer.data, 'Retrieve data successfully!', status.HTTP_200_OK


class CreateReplyCommentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @api_decorator
    def post(self, request):
        content = request.data.get('content')
        comment_id = request.data.get('comment_id')
        reply_comment = ReplyComment.objects.create(user=request.user, comment_id=comment_id, content=content)
        serializer = ReplyCommentSerializer(reply_comment, context={'request': request})
        return serializer.data, 'Reply comment successful!', status.HTTP_201_CREATED


class DeleteReplyCommentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @api_decorator
    def delete(self, request, pk):
        try:
            reply_comment = ReplyComment.objects.get(user=request.user, id=pk)
            reply_comment.delete()
            return {}, 'Successful!', status.HTTP_204_NO_CONTENT
        except Exception as e:
            print(e)
            return {}, 'That is not your comment!', status.HTTP_400_BAD_REQUEST


class UpdateReplyCommentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @api_decorator
    def put(self, request, pk):
        content = request.data.get('content')
        try:
            reply_comment = ReplyComment.objects.get(id=pk, user=request.user)
            reply_comment.content = content
            reply_comment.save()
            serializer = ReplyCommentSerializer(reply_comment, context={'request': request})
            return serializer.data, 'Update comment successful!', status.HTTP_200_OK
        except Exception as e:
            print(e)
            return {}, 'That is not your comment!'


class UploadFileAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    @api_decorator
    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['owner'] = str(request.user.id)

        # data = {'file': request.data.get('file')}
        # print(request.data.get('file'))
        # file_upload = FileUpload.objects.create(owner=request.user, file=request.data.get('file'))
        serializer = ImageUploadSerializer(data=data,
                                           context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            # serializer = ImageUploadSerializer(file_upload)
            return serializer.data, 'Upload successful!', status.HTTP_201_CREATED


class GetImgUser(APIView):
    permission_classes = [IsAuthenticated]

    @api_decorator
    def get(self, request):
        queryset = FileUpload.objects.all(owner=request.user)
        serializer = GetImageUploadSerializer(queryset, many=True,
                                              context={'request': request})
        return serializer.data, 'All image!', status.HTTP_200_OK


class AddImgForBlog(APIView):
    permission_classes = [IsAuthenticated]

    @api_decorator
    def post(self, request, pk):
        blog = Blog.objects.get(id=pk)
        image_id = request.data.get('image')
        file = FileUpload.objects.get(id=image_id)

        blog_img = BlogImage.objects.create(blog=blog, image=file)
        serializer = BlogImgSerializer(blog_img)
        return serializer.data, 'Add Image For Blog Successful!', status.HTTP_201_CREATED


class HistoryBlogAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @api_decorator
    def get(self, request):
        blog = Blog.objects.filter(user=request.user)
        serializer = BlogSerializer(blog, many=True, context={'request': request})
        return serializer.data, 'My history blog!', status.HTTP_200_OK


class HistoryLikeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @api_decorator
    def get(self, request):
        liked = Like.objects.filter(user=request.user)
        serializer = LikeSerializer(liked, many=True, context={'request': request})
        return serializer.data, 'History Like!', status.HTTP_200_OK
