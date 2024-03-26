# Generated by Django 4.2.11 on 2024-03-25 02:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import functools
import ultis.helper
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0006_replycomment'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileUpload',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('file_url', models.FileField(blank=True, null=True, upload_to=functools.partial(ultis.helper.custom_media_file_path, *(), **{'path': 'media'}))),
                ('file_type', models.TextField(blank=True, default='', max_length=500, null=True)),
                ('file_name', models.TextField(blank=True, default='', max_length=500, null=True)),
                ('file_extension', models.CharField(blank=True, max_length=500, null=True)),
                ('file_size', models.CharField(blank=True, max_length=500, null=True)),
                ('upload_finished_at', models.DateTimeField(blank=True, null=True)),
                ('video_duration', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('video_height', models.PositiveIntegerField(default=0)),
                ('video_width', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]