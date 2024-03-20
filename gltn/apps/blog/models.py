import uuid
from functools import partial

from django.db import models
from apps.user.models import CustomUser
from ultis.helper import custom_blog_image_path


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
    avatar_image_path = partial(custom_blog_image_path, path="avatar")
    avatar = models.ImageField(upload_to=avatar_image_path, null=True, blank=True)


class Like(BaseModel):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class Comment(BaseModel):
    content = models.CharField(max_length=500)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
