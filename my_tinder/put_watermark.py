from PIL import Image
from dating_site.settings import MEDIA_ROOT
import datetime


def put_watermark(image_path, watermark_path):

    base_image = Image.open(image_path)
    watermark_image = Image.open(watermark_path).convert('RGBA')
    datas = watermark_image.getdata()
    new_data: list = []

    for item in datas:

        if 50 <= item[0] <= 255 and 50 <= item[1] <= 255 and 50 <= item[1] <= 255:

            new_data.append((item[0], item[1], item[1], 0))
        else:

            new_data.append((item[0], item[1], item[1], 150))

    watermark_image.putdata(new_data)
    base_image.paste(watermark_image, box=(0, 150), mask=watermark_image)
    #base_image.save(f'{MEDIA_ROOT}/photos/%Y/%m/%d/new_Screenshot_{datetime.datetime.now()}.jpg')
    base_image.save(f'{image_path}')


