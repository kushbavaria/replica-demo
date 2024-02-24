import io
import base64
from PIL import Image


def image_to_base64(image):
    image_bytes = io.BytesIO()
    image.save(image_bytes, format='JPEG')
    image_bytes = image_bytes.getvalue()
    base64_encoded = base64.b64encode(image_bytes).decode('utf-8')

    return base64_encoded


def base64_to_image(base64_string):
    image_bytes = base64.b64decode(base64_string)
    image = Image.open(io.BytesIO(image_bytes))

    return image