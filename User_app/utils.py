import string
import random
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from home.models import CustomDesign
from django.conf import settings
import base64
from email.mime.image import MIMEImage
from io import BytesIO
import mimetypes

def generate_verification_code(length=5):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def send_verification_email(user, verification_code):
    context = {
        'user': user,
        'verification_code': verification_code,
        'company_name': 'ericPrint',
        'primary_color': '#b6c816',
        'secondary_color': '#6c757d',
    }

    custom_design = CustomDesign.objects.first()
    if custom_design:
        context['company_logo_cid'] = 'company_logo'

    subject = 'Verifikācijas kods'
    from_email = 'no-reply@ericprint.com'
    to_email = user.email

    text_content = render_to_string('emails/verification_email.txt', context)
    html_content = render_to_string('emails/verification_email.html', context)

    email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    email.attach_alternative(html_content, "text/html")

    if custom_design:
        with open(custom_design.image.path, 'rb') as img:
            mime_type, _ = mimetypes.guess_type(custom_design.image.path)
            mime_image = MIMEImage(img.read(), _subtype=mime_type.split('/')[1])
            mime_image.add_header('Content-ID', '<company_logo>')
            mime_image.add_header('Content-Disposition', 'inline', filename='company_logo.png')
            email.attach(mime_image)

    email.send()