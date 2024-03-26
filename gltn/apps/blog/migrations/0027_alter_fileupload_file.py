# Generated by Django 4.2.11 on 2024-03-25 08:06

from django.db import migrations, models
import functools
import ultis.helper


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0026_fileupload_owner_alter_fileupload_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileupload',
            name='file',
            field=models.ImageField(blank=True, null=True, upload_to=functools.partial(ultis.helper.custom_media_img_path, *(), **{'path': 'image'})),
        ),
    ]
