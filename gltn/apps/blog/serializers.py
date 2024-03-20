from rest_framework import serializers

from .models import Blog, Image, Like, Comment

from apps.user.serializers import UserSerializer


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id',
                  'avatar'
                  ]


class BlogSerializer(serializers.ModelSerializer):
    # user = UserSerializer()
    image = ImageSerializer(source='image_set', many=True, read_only=True)

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


class GetBlogSerializer(serializers.ModelSerializer):
    image = ImageSerializer(source='image_set', many=True, read_only=True)
    created_at = serializers.DateTimeField(format="%d/%m/%Y-%H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%d/%m/%Y-%H:%M:%S", read_only=True)

    class Meta:
        model = Blog
        fields = ['id',
                  'content',
                  'created_at',
                  'updated_at',
                  'image',
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


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    blog = GetBlogSerializer()

    class Meta:
        model = Comment
        fields = ['id',
                  'content',
                  'user',
                  'blog'
                  ]
