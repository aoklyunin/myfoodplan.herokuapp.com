# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-06-03 10:12
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0005_auto_20170603_1254'),
    ]

    operations = [
        migrations.CreateModel(
            name='InfoText',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, max_length=100000, null=True)),
                ('subText', models.TextField(blank=True, max_length=100000, null=True)),
                ('appendText', models.TextField(blank=True, max_length=100000, null=True)),
                ('caption', models.TextField(blank=True, max_length=100000, null=True)),
                ('pageName', models.TextField(blank=True, max_length=100000, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='dailyplan',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 6, 3, 13, 12, 17, 513131)),
        ),
        migrations.AlterField(
            model_name='product',
            name='dt',
            field=models.DateField(default=datetime.datetime(2017, 6, 6, 13, 12, 17, 507126)),
        ),
        migrations.AlterField(
            model_name='recipepart',
            name='tm',
            field=models.TimeField(default=datetime.datetime(2017, 6, 3, 13, 12, 17, 511629)),
        ),
        migrations.AlterField(
            model_name='remainportion',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 6, 3, 13, 12, 17, 505625)),
        ),
    ]