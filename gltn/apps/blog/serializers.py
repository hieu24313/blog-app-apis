from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ultis.file_helper import convert_file, file_size_in_mb
from .models import Blog, Image, Like, Comment, ImageComment, LikeComment, ReplyComment, FileUpload, BlogImage

from apps.user.serializers import UserSerializer


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id',
                  'avatar'
                  ]


class FileSerializer(serializers.ModelSerializer):
    # blog = BlogSerializerForImg()
    # image = GetImageUploadSerializer()

    class Meta:
        model = BlogImage
        fields = ['blog', 'image']


class ImageUploadSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d/%m/%Y-%H:%M:%S", read_only=True)

    class Meta:
        model = FileUpload
        fields = ['id',
                  'owner',
                  'file',
                  'file_content_type',
                  'file_name',
                  'file_size',
                  'created_at']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['file_size'] = file_size_in_mb(instance.file.size)
        # data['file'] = str(instance.file.url)
        data['file_url'] = self.context['request'].build_absolute_uri(data['file'])
        data['file_name'] = instance.file.name

        return data


class BlogSerializer(serializers.ModelSerializer):
    # user = UserSerializer()
    # image = ImageSerializer(source='image_set', many=True, read_only=True)
    # image = ImageUploadSerializer(source='blogimage_set__image', many=True, read_only=True)
    created_at = serializers.DateTimeField(format="%d/%m/%Y-%H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%d/%m/%Y-%H:%M:%S", read_only=True)

    class Meta:
        model = Blog
        fields = ['id',
                  'content',
                  'user',
                  'created_at',
                  'updated_at',
                  # 'image',
                  'count_like'
                  ]

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data['image'] = ImageUploadSerializer(FileUpload.objects.filter(blogimage__blog=instance), many=True, context=
                                                                                            self.context).data
        return data


class GetBlogSerializer(serializers.ModelSerializer):
    # image = ImageSerializer(source='image_set', many=True, read_only=True)
    created_at = serializers.DateTimeField(format="%d/%m/%Y-%H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%d/%m/%Y-%H:%M:%S", read_only=True)

    class Meta:
        model = Blog
        fields = ['id',
                  'content',
                  'created_at',
                  'updated_at',
                  # 'image',
                  'count_like'
                  ]


class ImageCreateSerializer(serializers.ModelSerializer):
    # blog = BlogSerializer()

    class Meta:
        model = Image
        fields = ['id',
                  'avatar',
                  'blog'
                  ]


class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    blog = GetBlogSerializer()

    class Meta:
        model = Like
        fields = ['id',
                  'user',
                  'blog'
                  ]


class ImageCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageComment
        fields = ['id',
                  'avatar',
                  'comment'
                  ]


class GetImageCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageComment
        fields = ['id',
                  'avatar',
                  ]


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    image = GetImageCommentSerializer(source='imagecomment_set', many=True, read_only=True)

    # blog = GetBlogSerializer()

    class Meta:
        model = Comment
        fields = ['id',
                  'content',
                  'user',
                  'image',
                  'count_like'
                  ]


class LikeCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeComment
        fields = ['id',
                  'user',
                  'comment']


class ReplyCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReplyComment
        fields = ['id',
                  'content',
                  'user',
                  'count_like',
                  'comment',
                  ]


# class BlogSerializer(serializers.ModelSerializer):
#     # user = UserSerializer()
#     image = ImageSerializer(source='image_set', many=True, read_only=True)
#
#     class Meta:
#         model = Blog
#         fields = ['id',
#                   'content',
#                   'user',
#                   'created_at',
#                   'updated_at',
#                   'image',
#                   'count_like'
#                   ]


class GetImageUploadSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d/%m/%Y-%H:%M:%S", read_only=True)

    class Meta:
        model = FileUpload
        fields = ['id',
                  'owner',
                  'file',
                  'file_content_type',
                  'file_name',
                  'file_size',
                  'created_at']


class BlogSerializerForImg(serializers.ModelSerializer):
    # user = UserSerializer()
    # image = ImageSerializer(source='image_set', many=True, read_only=True)

    class Meta:
        model = Blog
        fields = ['id',
                  'content',
                  'user',
                  'created_at',
                  'updated_at',
                  'image',
                  'count_like'
                  ]


class BlogImgSerializer(serializers.ModelSerializer):
    # blog = BlogSerializerForImg()
    # image = GetImageUploadSerializer()

    class Meta:
        model = BlogImage
        fields = ['blog', 'image']
