from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image
import base64

def save_base64_image(image_base64, filename):
    try:
        image_data = base64.b64decode(image_base64.split(',')[1])
        image_stream = BytesIO(image_data)
        image = Image.open(image_stream)

        if image.format not in ['JPEG', 'PNG']:
            raise Exception('Unsupported image format')

        image_io = BytesIO()
        image.save(image_io, format=image.format)
        image_file = ContentFile(image_io.getvalue(), name=filename)

        return image_file

    except Exception as e:
        return None