# Generated by Django 4.0.2 on 2022-05-18 21:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('my_tinder', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LikedUsers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='customuser',
            name='like',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Электронная почта'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='gender',
            field=models.CharField(choices=[('', 'Выберите пол'), ('Мужской', 'Мужской'), ('Женский', 'Женский')], max_length=7, verbose_name='Пол'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='liked_users',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='my_tinder.likedusers'),
        ),
    ]
