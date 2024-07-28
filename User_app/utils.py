import string
import random
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from home.models import CustomDesign
from django.conf import settings
import base64
from io import BytesIO

def generate_verification_code(length=5):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def get_image_base64(image_file):
    image_data = BytesIO(image_file.read())
    return base64.b64encode(image_data.getvalue()).decode('utf-8')

def send_verification_email(user, verification_code):
    context = {
        'user': user,
        'verification_code': verification_code,
        'company_name': 'ericPrint',
        'primary_color': '#b6c816',
        'secondary_color': '#6c757d',
    }

    custom_design = CustomDesign.objects.first()
    if custom_design and custom_design.image:
        with custom_design.image.open() as image_file:
            context['company_logo_base64'] = get_image_base64(image_file)


    subject = 'Verifikācijas kods'
    from_email = 'no-reply@ericprint.com'
    to_email = user.email

    text_content = render_to_string('emails/verification_email.txt', context)
    html_content = render_to_string('emails/verification_email.html', context)

    email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    email.attach_alternative(html_content, "text/html")
    email.send()