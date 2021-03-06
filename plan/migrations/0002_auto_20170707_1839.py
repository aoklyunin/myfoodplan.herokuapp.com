# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-07-07 15:39
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='eatEnable',
        ),
        migrations.AddField(
            model_name='recipe',
            name='eatParts',
            field=models.ManyToManyField(blank=True, to='plan.EatPart'),
        ),
        migrations.AlterField(
            model_name='dailyplan',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 7, 7, 18, 39, 32, 158015)),
        ),
        migrations.AlterField(
            model_name='recipepart',
            name='tm',
            field=models.TimeField(default=datetime.datetime(2017, 7, 7, 18, 39, 32, 157514)),
        ),
        migrations.AlterField(
            model_name='remainportion',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 7, 7, 18, 39, 32, 152010)),
        ),
    ]
