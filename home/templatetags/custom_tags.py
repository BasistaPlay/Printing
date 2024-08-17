from django import template
from home.models import CustomDesign

register = template.Library()

@register.simple_tag
def display_icon():
    try:
        icon = CustomDesign.objects.first()
        if icon and icon.image:
            return '{}'.format(icon.image.url)
        else:
            return ''
    except CustomDesign.DoesNotExist:
        return ''
    except Exception as e:

        return ''
