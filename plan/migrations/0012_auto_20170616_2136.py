# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-06-16 18:36
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0011_auto_20170616_2135'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='remain',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='dailyplan',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 6, 16, 21, 36, 45, 347068)),
        ),
        migrations.AlterField(
            model_name='recipepart',
            name='tm',
            field=models.TimeField(default=datetime.datetime(2017, 6, 16, 21, 36, 45, 345066)),
        ),
        migrations.AlterField(
            model_name='remainportion',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 6, 16, 21, 36, 45, 337561)),
        ),
    ]
