from django import template
from home.models import CustomDesign
import datetime

register = template.Library()

@register.simple_tag
def display_icon():
    try:
        icon = CustomDesign.objects.first()
        return '{}'.format(icon.image.url)
    except CustomDesign.DoesNotExist:
        return ''