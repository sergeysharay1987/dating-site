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


def get_middle_value(tup):
    return (tup[0] + tup[1] + tup[2]) // 3


def put_watermark(base_image: Image, watermark_path: str) -> BytesIO:
    """Накладывает водяной знак на изображение. В качестве водяного знака
    используется изображение с чёрным фоном, с расширением .png. Принимает два аргумента: изображение на которое
    нужно поместить водяной знак и изображение, содержащее водяной знак. Возвращает объект типа BytesIO. """
    base_image = base_image.convert('RGB')
    watermark_image: Image = Image.open(watermark_path).convert('RGBA')
    #datas = watermark_image.getdata()
    #datas = np.array(datas)
    datas = np.array(watermark_image)
    middle_pixels = datas.mean(axis=2)
    middle_values, counts = np.unique(middle_pixels, return_counts=True) # отбрасываем дублирующие элементы из
    # массива, содержащего средние значения цветов, а также получаем массив количества вхождений средних значений
    middle_values = middle_values[1:] # отбрасываем первый элемент - 0
    counts = counts[1:] # отбрасываем первый элемент - 0
    max_counts = np.max(counts)  # находим наибольшее количество вхождений
    i = np.where(counts == max_counts)  # находим индекс наиболее используемого цвета через массив вхождений,
    # так индексы массива для количества вхождений и массива средних значений цветов совпадают
    main_color = middle_values[i][0]
    print(middle_pixels)
    reshaped_datas = datas.reshape(-1, 3)

    print(f'reshaped_datas: {reshaped_datas.shape}')
    alpha_channel = np.where(reshaped_datas >= main_color, 70, 0) # получаем массив, содрежащий значения для альфа канала
    alpha_channel.dtype = 'uint8'
    new_datas = np.concatenate((reshaped_datas, alpha_channel), axis=1) # добавляем к каналам изображения (red, green, blue) альфа канал
    reshaped_new_datas = new_datas.reshape((datas.shape[0], -1, 4)) # изменяем форму массива, чтобы
    # использовать его в дальнейшем для получения объекта изображения PIL.Image.Image

    print(f'reshaped_new_datas.shape: {reshaped_new_datas.shape}')
    im = Image.fromarray(reshaped_new_datas, mode='RGBA')
    watermark_image.thumbnail((base_image.size[0] // 2, base_image.size[1] // 2))  # уменьшаем размеры водяного знака в
    # два раза меньше чем размеры базового изображения
    base_image.paste(watermark_image,
                     (base_image.size[0] - watermark_image.size[0], base_image.size[1] - watermark_image.size[1]),
                     mask=watermark_image)
    byte_io = BytesIO()
    byte_io.seek(0)
    base_image.save(byte_io, 'PNG')
    return byte_io
