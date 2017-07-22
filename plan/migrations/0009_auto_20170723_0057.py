# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-07-22 21:57
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0008_auto_20170723_0017'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='defaultCapacity',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='dailyplan',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 7, 23, 0, 57, 21, 712057)),
        ),
        migrations.AlterField(
            model_name='recipepart',
            name='tm',
            field=models.TimeField(default=datetime.datetime(2017, 7, 23, 0, 57, 21, 711556)),
        ),
        migrations.AlterField(
            model_name='remainportion',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 7, 23, 0, 57, 21, 706054)),
        ),
    ]