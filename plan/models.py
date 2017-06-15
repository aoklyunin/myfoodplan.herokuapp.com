# -*- coding: utf-8 -*-
import datetime

from django.contrib.auth.models import User
from django.db import models


class InfoText(models.Model):
    text = models.TextField(max_length=100000, null=True, blank=True)
    subText = models.TextField(max_length=100000, null=True, blank=True)
    appendText = models.TextField(max_length=100000, null=True, blank=True)
    caption = models.TextField(max_length=100000, null=True, blank=True)
    pageName = models.TextField(max_length=100000, null=True, blank=True)

    def __str__(self):
        return self.pageName


# приёмы пищи
class EatPart(models.Model):
    name = models.CharField(max_length=300, default="")

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


# типы продуктов
class ProductType(models.Model):
    name = models.CharField(max_length=300, default="")

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class RemainPortion(models.Model):
    # кол-во
    cnt = models.IntegerField(default=1)
    # дата изготовления
    date = models.DateField(default=datetime.datetime.now())

    def __str__(self):
        return str(self.cnt) + ":" + str(self.date)

    def __unicode__(self):
        return str(self.cnt) + ":" + str(self.date)


# продукты
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
    # кол-во в упаковке
    cnt = models.IntegerField(default=1)
    # оставшиеся продукты
    products = models.ManyToManyField(RemainPortion)
    # срок годности
    dt = models.FloatField(default=3)
    # содержание воды
    water = models.FloatField(default=0)

    def __str__(self):
        return str(self.name) + "(" + str(self.dimention) + ")"

    def __unicode__(self):
        return str(self.name) + "(" + str(self.dimention) + ")"


# порция продукта
class ProductPortion(models.Model):
    product = models.ForeignKey(Product)
    count = models.FloatField(default=0)

    def __str__(self):
        return str(self.product.name) + "(" + str(self.count) + " " + str(self.product.dimention) + ")"

    def __unicode__(self):
        return str(self.product.name) + "(" + str(self.count) + " " + str(self.product.dimention) + ")"


# блюдо
class Recipe(models.Model):
    # имя
    name = models.CharField(max_length=10000, default="")
    # инструкция
    instruction = models.CharField(max_length=10000, default="")
    # продукты
    products = models.ManyToManyField(ProductPortion, blank=True, default=None)
    # белки на 100 г.
    proteins = models.FloatField(default=0)
    # жиры на 100 г.
    fats = models.FloatField(default=0)
    # углеводы на 100 г.
    carbohydrates = models.FloatField(default=0)
    # калорийность на 100 г.
    caloricity = models.FloatField(default=0)
    # когда можно употреблять
    # определяется по маске первый бит - завтрак, второй бит - второй завтрак,
    # третий - обед, четвёртый - полдник, пятый - ужин
    # если 0 - можно, если 1 - нет
    eatEnable = models.IntegerField(default=0)
    # можно ли сейчас формировать меню с рецаптами
    access = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


# часть блюда
class RecipePart(models.Model):
    recipes = models.ManyToManyField(Recipe)
    cnt = models.FloatField(default=0)
    eatPart = models.ForeignKey(EatPart)
    tm = models.TimeField(default=datetime.datetime.now())

    def __str__(self):
        return str(self.eatPart) + " " + str(self.cnt) + " " + str(self.tm)

    def __unicode__(self):
        return str(self.eatPart) + " " + str(self.cnt) + " " + str(self.tm)


class DailyPlan(models.Model):
    date = models.DateField(default=datetime.datetime.today())
    rParts = models.ManyToManyField(RecipePart)
