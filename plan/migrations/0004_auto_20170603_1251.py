# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-06-03 09:51
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0003_auto_20170603_1230'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='water',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='dailyplan',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 6, 3, 12, 51, 21, 687952)),
        ),
        migrations.AlterField(
            model_name='product',
            name='dt',
            field=models.DateField(default=datetime.datetime(2017, 6, 6, 12, 51, 21, 683449)),
        ),
        migrations.AlterField(
            model_name='recipepart',
            name='tm',
            field=models.TimeField(default=datetime.datetime(2017, 6, 3, 12, 51, 21, 686951)),
        ),
        migrations.AlterField(
            model_name='remainportion',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 6, 3, 12, 51, 21, 682448)),
        ),
    ]
