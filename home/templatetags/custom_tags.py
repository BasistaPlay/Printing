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
            return ''  # Return a default value or empty string if no image
    except CustomDesign.DoesNotExist:
        return ''  # Handle the case where no CustomDesign records are found
    except Exception as e:
        # Log the error for further inspection or return a default value
        # You might use Django's logging framework here
        return ''  # Handle unexpected exceptions gracefully
