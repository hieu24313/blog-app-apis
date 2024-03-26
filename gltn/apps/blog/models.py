import uuid
from functools import partial

from django.db import models
from apps.user.models import CustomUser
from ultis.helper import custom_blog_image_path, custom_comment_image_path, custom_media_file_path, \
    custom_media_img_path


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_active = models.BooleanField(default=True)
    # tự tạo giá trị lúc tạo record
    created_at = models.DateTimeField(auto_now_add=True)
    # tự tạo giá trị lúc update record
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Blog(BaseModel):
    content = models.CharField(max_length=500, null=True, blank=True)
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)
    count_like = models.PositiveIntegerField(default=0)


class Image(BaseModel):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    blog = models.ForeignKey(Blog, null=True, on_delete=models.CASCADE)
    avatar_image_path = partial(custom_blog_image_path, path="image")
    avatar = models.ImageField(upload_to=avatar_image_path, null=True, blank=True)


class Like(BaseModel):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class Comment(BaseModel):
    content = models.CharField(max_length=500)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    count_like = models.PositiveIntegerField(default=0)


class ReplyComment(BaseModel):
    content = models.CharField(max_length=500)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    count_like = models.PositiveIntegerField(default=0)


class ImageComment(BaseModel):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    avatar_image_path = partial(custom_comment_image_path, path="image")
    avatar = models.ImageField(upload_to=avatar_image_path, null=True, blank=True)


class LikeComment(BaseModel):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class FileUpload(BaseModel):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)

    file_path = partial(custom_media_img_path, path="image")
    file = models.FileField(upload_to=file_path, null=True, blank=True)

    file_url = models.CharField(null=True, blank=True, max_length=500)
    file_content_type = models.TextField(default='', null=True, blank=True, max_length=500)
    file_name = models.TextField(default='', null=True, blank=True, max_length=500)
    file_extension = models.CharField(null=True, blank=True, max_length=500)
    file_size = models.CharField(null=True, blank=True, max_length=500)

    # upload_finished_at = models.DateTimeField(blank=True, null=True)
    # video_duration = models.PositiveIntegerField(default=0, null=True, blank=True)

    # video_height = models.PositiveIntegerField(default=0)
    # video_width = models.PositiveIntegerField(default=0)


class BlogImage(BaseModel):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    image = models.ForeignKey(FileUpload, on_delete=models.SET_NULL, blank=True, null=True)



