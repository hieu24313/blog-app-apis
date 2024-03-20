import math
import os
import re
import smtplib
import uuid
from collections import OrderedDict
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
# from phonenumbers import is_valid_number, parse
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
import requests
from django.core.files.base import ContentFile

from gltn import settings


def validate_email_address(email_address):
    return re.search(r"^[A-Za-z0-9_!#$%&'*+\/=?`{|}~^.-]+@[A-Za-z0-9.-]+$", email_address)


def get_validate_date(current_date):
    if current_date:
        return current_date.strftime("%d/%m/%Y")
    else:
        return ''


def get_full_image_url(request, file_path):
    if settings.USE_S3:
        return file_path

    domain = request.META['HTTP_HOST']
    full_url = f"http://{domain}{file_path}"
    return full_url


# def convert_phone_number(raw_phone_number):
#     if raw_phone_number[0] == '0':
#         phone_number = '+84' + raw_phone_number[1:]
#     else:
#         phone_number = '+' + raw_phone_number
#
#     phone_number = parse(phone_number, None)
#     is_valid_number(phone_number)
#
#     return phone_number


def custom_user_image_path(instance, filename, path='general'):
    instance_id = str(instance.id)
    upload_path = os.path.join(f'user_media/images/{path}/', instance_id)
    new_filename = f'{uuid.uuid4()}{os.path.splitext(filename)[1]}'
    return os.path.join(upload_path, new_filename)


def custom_blog_image_path(instance, filename, path='general'):
    instance_id = str(instance.id)
    upload_path = os.path.join(f'blog_media/images/{path}/', instance_id)

    new_filename = f'{uuid.uuid4()}{os.path.splitext(filename)[1]}'
    return os.path.join(upload_path, new_filename)


def is_valid_image(image_field):
    try:
        return image_field and default_storage.exists(image_field.name)
    except:
        return False


def create_image_array(data, instance):
    image_urls = []
    for i in range(1, 6):
        image_field_name = f'image_desc{i}'
        image_field = getattr(instance, image_field_name) if hasattr(instance, image_field_name) else None
        if image_field and is_valid_image(image_field):
            image_urls.append(data[image_field_name])
        data.pop(image_field_name, None)

    data['images'] = image_urls
    return data


class CustomPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 500
    page_query_param = 'page'

    def __init__(self):
        self.total_record = 0

    def add_total_record(self, total_record):
        self.total_record = total_record

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('total_page', math.ceil(self.page.paginator.count / 10)),
            ('num_record', len(self.page.object_list)),
            ('total_record', self.total_record),
            ('current_page', self.page.number),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))


from threading import Thread


def send_email(emails, subject, content):
    thread = Thread(target=send_email_thread, args=(emails, subject, content))
    thread.start()


def send_email_thread(emails, subject, content):
    html_content = f"<html><body>{content}</body></html>"

    message = MIMEMultipart()
    message['From'] = settings.EMAIL_HOST_USER
    message['To'] = ", ".join(emails)
    message['Subject'] = subject

    message.attach(MIMEText(html_content, 'html'))

    try:
        server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        server.starttls()
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        server.sendmail(settings.EMAIL_HOST_USER, emails, message.as_string())
        server.quit()
    except Exception as e:
        print(e)


def validate_image_format(value):
    if value:
        allowed_formats = ('image/jpeg', 'image/png')
        if value.content_type not in allowed_formats:
            raise ValidationError("Invalid image format. Only JPEG and PNG are accepted.")

        if value.size > 5 * 1024 * 1024:  # 5MB file size limit
            raise ValidationError("Image size is too large. The limit is 5MB.")


def download_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        return ContentFile(response.content)
    return None


def convert_unicode_text(text):
    patterns = {
        '[àáảãạăắằẵặẳâầấậẫẩ]': 'a',
        '[đ]': 'd',
        '[èéẻẽẹêềếểễệ]': 'e',
        '[ìíỉĩị]': 'i',
        '[òóỏõọôồốổỗộơờớởỡợ]': 'o',
        '[ùúủũụưừứửữự]': 'u',
        '[ỳýỷỹỵ]': 'y'
    }
    """
    Convert from 'Tieng Viet co dau' thanh 'Tieng Viet khong dau'
    text: input string to be converted
    Return: string converted
    """
    output = text
    for regex, replace in patterns.items():
        output = re.sub(regex, replace, output)
        output = re.sub(regex.upper(), replace.upper(), output)

    return output
