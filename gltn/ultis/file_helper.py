from django.template.defaultfilters import filesizeformat
from rest_framework.exceptions import ValidationError


def convert_file(size):
    file_size = int(size) / 1024
    return f'{file_size} kb'


def file_size_in_mb(size_in_bytes):
    max_size = 1 * 1024 * 1024 * 1024  # 1GB
    if size_in_bytes > max_size:
        raise ValidationError("File size cannot exceed 1GB.")
    return filesizeformat(size_in_bytes)
