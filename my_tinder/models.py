from django.db.models import CharField, ImageField
from django.contrib.auth.models import User


class Client(User):
    MALE = 'М'
    FEMALE = 'Ж'
    GENDERS = ((MALE, 'Мужчина'),
               (FEMALE, 'Женщина'))

    avatar = ImageField(verbose_name='Фото', upload_to='photos/%Y/%m/%d')
    gender = CharField(verbose_name='Пол', max_length=7, choices=GENDERS)

    class Meta:
        verbose_name = 'Участники'
        verbose_name_plural = 'Участники'
