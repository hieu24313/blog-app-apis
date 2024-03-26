import secrets
from functools import partial

import jwt

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager, BaseUserManager
from datetime import datetime, timedelta, date
import uuid

from django.utils.functional import cached_property
from django.utils.html import format_html

from ultis.helper import custom_user_image_path


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, **extra_fields):
        if not phone_number:
            raise ValueError('User must have a phone number.')

        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(extra_fields.get('password', secrets.token_urlsafe(6)))
        user.save()
        return user

    def create_superuser(self, phone_number, **extra_fields):
        # Kiểm tra xem phone_number đã tồn tại chưa
        if self.model.objects.filter(phone_number=phone_number).exists():
            raise ValueError('Phone number already exists for a regular user.')

        user = self.create_user(phone_number, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = (
        ('Male', 'Nam'),
        ('Female', 'Nữ'),
        ('Unknown', ''),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=200, blank=True)
    username = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=255, unique=True, db_index=True, null=True)
    email = models.EmailField(null=True, blank=True)
    avatar_image_path = partial(custom_user_image_path, path="avatar")
    avatar = models.ImageField(upload_to=avatar_image_path, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    # tự tạo giá trị lúc tạo record
    created_at = models.DateTimeField(auto_now_add=True)
    # tự tạo giá trị lúc update record
    updated_at = models.DateTimeField(auto_now=True)

    gender = models.CharField(max_length=7, choices=GENDER_CHOICES, default='Unknown')

    USERNAME_FIELD = 'phone_number'

    objects = CustomUserManager()

    def __str__(self):
        return self.full_name

    @cached_property
    def player_avatar(self):
        html = '<img src="{img}" style="max-width: 100px; height: auto; display: block; margin: 0 auto;">'
        if self.avatar:
            return format_html(html, img=self.avatar.url)
        return format_html('<strong>There is no image for this entry.<strong>')

    player_avatar.short_description = 'Avatar'

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': str(self.pk),
            'exp': int(dt.timestamp())
        }, settings.SECRET_KEY, algorithm='HS256')

        return token

    @property
    def token(self):
        return self._generate_jwt_token()

    @property
    def new_password(self):
        new_pwd = secrets.token_urlsafe(6)
        self.set_password(new_pwd)
        self.save()
        return new_pwd

    @property
    def raw_phone_number(self):
        return str(self.phone_number) if self.phone_number else ""

    # class Meta:
    #     verbose_name = "User"
    #     verbose_name_plural = "Users"


class LetterAvatar(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=10, blank=True)
    image = models.ImageField(upload_to='letter-avatar-images')

