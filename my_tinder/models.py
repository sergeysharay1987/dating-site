from cuser.models import AbstractCUser
from django.db.models import CharField, ImageField, ManyToManyField, TextChoices


class Gender(TextChoices):
    MALE = 'М', 'Мужчина'
    FEMALE = 'Ж', 'Женщина'


class CustomUser(AbstractCUser):

    avatar = ImageField(verbose_name='Фото', upload_to='photos/%Y/%m/%d', blank=True, null=True)
    gender = CharField(verbose_name='Пол', max_length=1, choices=Gender.choices)
    liked_users = ManyToManyField('self', blank=True, symmetrical=False, related_name='liked_users_set')
    unliked_users = ManyToManyField('self', blank=True, symmetrical=False, related_name='unliked_users_set')

    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'
