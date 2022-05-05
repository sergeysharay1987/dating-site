import os

from PIL.Image import Image
from PIL import Image
from io import BytesIO
import numpy as np

'''def put_watermark(base_image: Image, watermark_path: str) -> BytesIO:
    """Накладывает водяной знак на изображение. В качестве водяного знака
    используется изображение с чёрным фоном, с расширением .png. Принимает два аргумента: изображение на которое
    нужно поместить водяной знак и изображение, содержащее водяной знак. Возвращает объект типа BytesIO. """
    base_image = base_image.convert('RGB')
    watermark_image: Image = Image.open(watermark_path).convert('RGBA')
    middle_pixels: list = []

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
    watermark_image.thumbnail((base_image.size[0]//2, base_image.size[1]//2))  # уменьшаем размеры водяного знака в
    # два раза меньше чем размеры базового изображения
    base_image.paste(watermark_image,
                     (base_image.size[0] - watermark_image.size[0], base_image.size[1] - watermark_image.size[1]),
                     mask=watermark_image)
    byte_io = BytesIO()
    byte_io.seek(0)
    base_image.save(byte_io, 'PNG')
    return byte_io'''


def put_watermark(base_image: Image, watermark_path: str) -> BytesIO:
    if base_image.mode != 'RGBA':

        base_image = base_image.convert('RGBA')
    watermark_img: Image = Image.open(watermark_path)
    width, heigth = base_image.size
    watermark_img.thumbnail((width//3, heigth//3))
    destination = (width - watermark_img.size[0], 0)
    base_image.alpha_composite(watermark_img, destination)
    byte_io = BytesIO()
    byte_io.seek(0)
    base_image.save(byte_io, 'PNG')
    base_image.show()
    return byte_io
