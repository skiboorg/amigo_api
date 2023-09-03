from PIL import Image
from io import BytesIO
from django.core.mail import send_mail
from django.template.loader import render_to_string

import settings


def create_thumb(image):
    fill_color = '#fff'
    base_image = Image.open(image)
    if base_image.mode in ('RGBA', 'LA'):
        background = Image.new(base_image.mode[:-1], base_image.size, fill_color)
        background.paste(base_image, base_image.split()[-1])
        base_image = background
    blob = BytesIO()
    width, height = base_image.size
    transparent = Image.new('RGB', (width, height), (0, 0, 0, 0))
    transparent.paste(base_image, (0, 0))
    transparent.thumbnail((120, 120), Image.LANCZOS)

    transparent.save(blob, 'JPEG', quality=100)
    return blob


def send_email(obj):
    msg_html = render_to_string('form_notify.html', {'obj': obj})
    send_mail('Заполнена форма', None, settings.YA_USER, [settings.MAIL_TO],
              fail_silently=False, html_message=msg_html)