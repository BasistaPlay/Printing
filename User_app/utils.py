import string
import random
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from home.models import CustomDesign

def generate_verification_code(length=5):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def send_verification_email(user, verification_code):
    context = {
        'user': user,
        'verification_code': verification_code,
        'company_name': 'ericPrint',
        'primary_color': '#007bff',
        'secondary_color': '#6c757d',
    }

    custom_design = CustomDesign.objects.first()
    if custom_design:
        context['company_logo_url'] = custom_design.image.url

    subject = 'Verifikācijas kods'
    from_email = 'info@ericprint.com'
    to_email = user.email

    html_content = render_to_string('emails/verification_email.html', context)

    email = EmailMultiAlternatives(subject, '', from_email, [to_email])
    email.attach_alternative(html_content, "text/html")
    email.send()