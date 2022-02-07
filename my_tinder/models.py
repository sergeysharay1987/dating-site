from django.db.models import Model, CharField, ImageField, EmailField

# Create your models here.


class Client(Model):
    MALE = 'М'
    FEMALE = 'Ж'
    GENDERS = ((MALE, 'Мужчина'),
               (FEMALE, 'Женщина'))

    avatar = ImageField(verbose_name='Фото', upload_to='photos/%Y/%m/%d')
    gender = CharField(verbose_name='Пол', max_length=7, choices=GENDERS)
    first_name = CharField(verbose_name='Имя', max_length=50)
    second_name = CharField(verbose_name='Фамилия', max_length=50)
    email = EmailField(verbose_name='Электронная почта', unique=True)
