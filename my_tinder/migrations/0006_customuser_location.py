# Generated by Django 4.0.5 on 2022-11-25 18:55

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_tinder', '0005_customuser_latitude_customuser_longitude'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326),
        ),
    ]
