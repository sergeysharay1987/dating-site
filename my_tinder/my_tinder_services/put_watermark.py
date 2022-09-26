from PIL.Image import Image
from PIL import Image
from io import BytesIO


def put_watermark(base_image: Image, watermark_path: str) -> BytesIO:
    if base_image.mode != 'RGBA':

        base_image = base_image.convert('RGBA')
    watermark_image: Image = Image.open(watermark_path)
    width, heigth = base_image.size
    watermark_image.thumbnail((width//3, heigth//3))
    destination = (width - watermark_image.size[0], 0)
    base_image.alpha_composite(watermark_image, destination)
    byte_io = BytesIO()
    byte_io.seek(0)
    base_image.save(byte_io, 'PNG')
    return byte_io
