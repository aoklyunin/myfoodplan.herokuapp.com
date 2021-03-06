# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-07-22 19:14
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0005_auto_20170707_2126'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='tp',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='plan.RecipeType'),
        ),
        migrations.AlterField(
            model_name='dailyplan',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 7, 22, 22, 14, 8, 899399)),
        ),
        migrations.AlterField(
            model_name='recipepart',
            name='tm',
            field=models.TimeField(default=datetime.datetime(2017, 7, 22, 22, 14, 8, 898430)),
        ),
        migrations.AlterField(
            model_name='remainportion',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 7, 22, 22, 14, 8, 891509)),
        ),
    ]
