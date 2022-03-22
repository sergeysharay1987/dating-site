from PIL.Image import Image
from PIL import Image
from io import BytesIO


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


def make_size(base_img: Image, watermark_img: Image):
    """Подгоняет изображение с водяным знаком под базовое изображение"""
    # base_img: Image = Image.open(base_img_path)  # базовое изображение - для вставки водяного знака
    # watermark_img: image = Image.open(
    # watermark_img_path)  # изображение, содержащее водяной знак, оно должно иметь белый
    # фон, для того чтобы в последующем сделать белый цвет полностью прозрачным
    watermark: Image = Image.new('RGB', base_img.size, (128, 128, 128, 0))  # создаём новое изображение, полностью белое,
    # для того чтобы вставить в него изображение с водяным знаком,
    # здесь также используется белый цвет, чтобы в дальнейшем сделать его полностью прозрачным
    watermark_width, watermark_height = watermark_img.size  # получаем размеры изображение, содержащее водяной знак
    watermark_size = watermark_width // 4, watermark_height // 4  # создаём кортеж с размерами, уменьшая размеры
    # изображения с водяным знаком в 4 раза
    watermark_img = watermark_img.resize(watermark_size)  # уменьшаем в 4 раза наш водяной знак, для того чтобы он не
    # занимал много места на базовом изображении
    # watermark.alpha_composite(watermark_img)
    watermark.paste(watermark_img, (watermark.size[0] - watermark_img.size[0], 0))  # вставляем уменьшенный водяной
    # знак в полностью белое изображение
    print(watermark.mode)
    return watermark


def put_watermark(base_image: Image, watermark_path: str):
    # base_image = Image.open(image_path)
    # print(f'image_in_put_watermark_function{image}')
    base_image = base_image.convert('RGB')
    watermark_image = Image.open(watermark_path).convert('RGBA')
    #watermark = Image.new('RGBA', watermark_image.size, (128, 128, 128, 0))

    #    pos_watermark = (back_watermark.size[0]-720, back_watermark.size[1]-750)
    # print(pos_watermark)
    #watermark.paste(watermark_image)
    datas = watermark_image.getdata()
    # watermark.show()
    new_data: list = []

    for item in datas:
        #if item[0] == 128 and item[1] == 128 and item[2] == 128:
        if (item[0] != 0 and item[1] != 0 and item[2] != 0):
        # if item[0] == 0 and item[1] == 0 and item[2] == 0:
        #if item[0] == 255 and item[1] == 255 and item[2] == 255:
        #if 250 <= item[0] <= 255 and 250 <= item[1] <= 255 and 250 <= item[2] <= 255:
            #new_data.append((item[0], item[1], item[2], 150))
            new_data.append((item[0], item[1], item[2], 150))
            #new_data.append((0, 0, 0, 0))
        #else:
        elif (item[0] == 0 and item[1] == 0 and item[2] == 0) or (item[0] <= 150 or item[1] <= 150 or item[2] <= 150):
            new_data.append((0, 0, 0, 0))
            #new_data.append((0, 0, 0, 0))

    watermark_image.putdata(new_data)
    #watermark_image = make_size(base_image, watermark_image)
    print(f'watermark_image: {watermark_image}')
    watermark_image.show()
    base_image.paste(watermark_image, mask=watermark_image)
    base_image.show()
    byte_io = BytesIO()
    byte_io.seek(0)
    base_image.save(byte_io, 'PNG')
    return byte_io


# def put_watermark(image: Image, watermark_path: str):
#     # base_image = Image.open(image_path)
#     # print(f'image_in_put_watermark_function{image}')
#     image = image.convert('RGB')
#     watermark_image = Image.open(watermark_path).convert('RGB')
#     watermark = Image.new('RGBA', watermark_image.size, (255, 255, 255, 255))
#     #    pos_watermark = (back_watermark.size[0]-720, back_watermark.size[1]-750)
#     # print(pos_watermark)
#     watermark.paste(watermark_image)
#     datas = watermark_image.getdata()
#     # watermark.show()
#     new_data: list = []
#
#     for item in datas:
#
#         if item[0] == 255 and item[1] == 255 and item[2] == 255:
#         #if 250 <= item[0] <= 255 and 250 <= item[1] <= 255 and 250 <= item[2] <= 255:
#
#             new_data.append((item[0], item[1], item[2], 0))
#         else:
#
#             new_data.append((item[0], item[1], item[2], 50))
#     watermark.putdata(new_data)
#     watermark.show()
#     watermark = watermark.resize((watermark.size[0] // 2, watermark.size[1] // 2))
#     pos_water = (image.size[0] - watermark.size[0], image.size[1] - watermark.size[1])
#     image.paste(watermark, box=pos_water, mask=watermark)
#     image.show()
#     byte_io = BytesIO()
#     byte_io.seek(0)
#     image = image.save(byte_io, 'PNG')
#     # print(f'image_after_pasting_watermark: {image}')
#     # image.show()
#     print(f'watermarked_image___________________: {byte_io}')
#     # image.show()
#     return byte_io