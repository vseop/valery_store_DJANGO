from io import BytesIO
import sys
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile


def upload_function(instance, filename):
    """Путь для сохранения галереи изображений"""
    return f"{instance.__class__.__name__.lower()}/{instance.product.slug}/{filename}"


def upload_function_poster(instance, filename):
    """Путь для сохранения Постера"""
    return f"{instance.__class__.__name__.lower()}/{instance.slug}/{filename}"


def new_image_field(obj, x, y):
    """Обрезаем и уменьшаем загружаемые изображения"""
    img = Image.open(obj)
    new_image = img.convert('RGB')
    new_image.thumbnail((x, y))
    filestream = BytesIO()
    new_image.save(filestream, 'JPEG')  # quality=90
    filestream.seek(0)
    obj = InMemoryUploadedFile(
        filestream, 'ImageField', obj.name, 'jpeg/image', sys.getsizeof(filestream), None
    )
    return obj
