# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models


class ProductType(models.Model):
    name = models.CharField(max_length=300, default="")


class Product(models.Model):
    # единица измерения
    dimention = models.CharField(max_length=200, default="г.")
    # имя
    name = models.CharField(max_length=200, default="")
    # белки на 100 г.
    proteins = models.FloatField(default=0)
    # жиры на 100 г.
    fats = models.FloatField(default=0)
    # углеводы на 100 г.
    carbohydrates = models.FloatField(default=0)
    # калорийность на 100 г.
    caloricity = models.FloatField(default=0)
    # тип
    tp = models.ForeignKey(ProductType)

class ProductPortion(models.Model):
    product = models.ForeignKey(Product)
    count = models.FloatField(default=0)


class Recipe(models.Model):
    instruction = models.CharField(max_length=10000,defult="")
    products = M