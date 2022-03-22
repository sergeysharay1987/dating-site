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
    middle_pixels = []
    #base_image = Image.open(image_path).convert('RGB')
    watermark_image = Image.open(watermark_path).convert('RGBA')
    datas = watermark_image.getdata()
    for item in datas:  # получаем значения каналов red, green, blue, aplpha
        middle_pixel = (item[0] + item[1] + item[2]) // 3  # ищем среднее-арифметическое каналов (red+green+blue)/3
        # alpha канал не учитываем, так как он отвечает за
        # прозрачность
        if middle_pixel != 0:  # если среднее-арифметическое не равно 0 (если цвет - не чёрный), то добавляем его в
            # список
            middle_pixels.append(middle_pixel)
    set_middle_values = set(middle_pixels)  # преобразуем список в множество (убираем повторяющиеся значения),
    # чтобы узнать какие цвета присутствуют в изображении
    number_occurrences = []  # создаём список вхождений, в него будем класть кортеж из 2-х элементов:
    # среднее-арифметическое (red+green+blue)/3 и кол-во вхождений этого среднего-арифметического в изображение
    for value in set_middle_values:
        number_occurrences.append((value, middle_pixels.count(value)))  # кладём среднее-арифметическое
        # (red+green+blue)/3 и кол-во вхождений этого среднего арифметического в изображение
    number_occurence = max(number_occurrences, key=lambda x: x[1])  # находим среднее-арифметическое наиболее
    # используемого цвета в изображении,
    # найдя максимальное число среди кол-ва вхождений
    main_color = number_occurence[0]  # получаем среднее-арифметическое наиболее часто используемого цвета в изображении
    new_data: list = []  # создаём список, чтобы класть в него новые значения каналов (red, green, blue,
    # alpha) пикселей изображения

    for item in datas:

        if item[0] + item[1] + item[2] / 3 >= main_color:  # если среднее-арифметическое каналов red, green, blue
            # больше или равно среднему-арифметическому значению наиболее используемого цвета, то делаем цвет
            # полупрозрачным

            new_data.append((item[0], item[1], item[2], 70))
        else:  # иначе, делаем цвет
            # полностью прозрачным
            new_data.append((item[0], item[1], item[2], 0))
    watermark_image.putdata(new_data)

    watermark_image = watermark_image.resize((watermark_image.size[0] // 2, watermark_image.size[1] // 2))

    base_image.paste(watermark_image,
                     (base_image.size[0] - watermark_image.size[0], base_image.size[1] - watermark_image.size[1]),
                     mask=watermark_image)
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