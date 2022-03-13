from PIL.Image import Image
from PIL import Image
from io import BytesIO
from PIL.ImageFile import ImageFile
from io import BytesIO

# from dating_site.settings import MEDIA_ROOT
# import datetime
# import os
from PIL.JpegImagePlugin import JpegImageFile

'''def put_watermark(image_path, watermark_path):

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
    base_image.save(f'{image_path}')'''


def put_watermark(image: Image, watermark_path: str):
    # base_image = Image.open(image_path)
    #print(f'image_in_put_watermark_function{image}')
    image = image.convert('RGB')
    watermark_image = Image.open(watermark_path).convert('RGB')
    watermark = Image.new('RGBA', watermark_image.size, (255, 255, 255, 255))
    #    pos_watermark = (back_watermark.size[0]-720, back_watermark.size[1]-750)
    # print(pos_watermark)
    watermark.paste(watermark_image)
    datas = watermark_image.getdata()
    #watermark.show()
    new_data: list = []

    for item in datas:

        if item[0] != 255 and item[1] != 255 and item[1] != 255:

            new_data.append((item[0], item[1], item[2], 0))
        else:

            new_data.append((item[0], item[1], item[2], 50))
    watermark.putdata(new_data)
    watermark.show()
    watermark = watermark.resize((watermark.size[0] // 2, watermark.size[1] // 2))
    pos_water = (image.size[0] - watermark.size[0], image.size[1] - watermark.size[1])
    image.paste(watermark, box=pos_water, mask=watermark)
    image.show()
    byte_io = BytesIO()
    byte_io.seek(0)
    image = image.save(byte_io, 'PNG')
    #print(f'image_after_pasting_watermark: {image}')
    #image.show()
    print(f'watermarked_image___________________: {byte_io}')
    #image.show()
    return byte_io
