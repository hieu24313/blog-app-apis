# Generated by Django 4.2.11 on 2024-03-25 06:17

from django.db import migrations, models
import functools
import ultis.helper


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_fileupload_file_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileupload',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=functools.partial(ultis.helper.custom_blog_image_path, *(), **{'path': 'image'})),
        ),
    ]
