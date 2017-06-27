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


# типы продуктов
class RecipeType(models.Model):
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
    # остаток
    remain = models.FloatField(default=0)

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
    # вес
    weight = models.FloatField(default=0)
    # воды
    water = models.FloatField(default=0)
    # когда можно употреблять
    # определяется по маске первый бит - завтрак, второй бит - второй завтрак,
    # третий - обед, четвёртый - полдник, пятый - ужин
    # если 0 - можно, если 1 - нет
    eatEnable = models.IntegerField(default=0)
    # можно ли сейчас формировать меню с рецаптами
    access = models.BooleanField(default=True)
    # остаток на складе
    remain = models.FloatField(default=0)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def generateData(self):
        arr = []
        for ns in self.products.all():
            if (ns.product != None):
                arr.append({'product': str(ns.product.pk),
                            'cnt': str(ns.count)})
        return arr

    def addFromFormset(self, formset, doCrear=False):
        if (doCrear):
            for ns in self.products.all():
                ns.delete()
            self.products.clear()

        if formset.is_valid():
            self.proteins = 0
            self.fats = 0
            self.carbohydrates = 0
            self.caloricity = 0
            self.weight = 0
            self.water = 0

            for form in formset.forms:
                if form.is_valid:
                    try:
                        d = form.cleaned_data
                        ns = ProductPortion.objects.create(product=Product.objects.get(pk=int(d["product"])),
                                                           count=float(d["cnt"]))
                        ns.save()
                        # print(d["cnt"])
                        self.products.add(ns)
                        p = Product.objects.get(pk=int(d["product"]))
                        self.proteins += p.proteins * d["cnt"] * 10
                        self.fats += p.fats * d["cnt"] * 10
                        self.carbohydrates += p.carbohydrates * d["cnt"] * 10
                        self.caloricity += p.caloricity * d["cnt"] * 10
                        print(p.caloricity)
                        print(d["cnt"])
                        print(d["cnt"] * p.caloricity)
                        print(p.caloricity * d["cnt"] * 10)
                        print("--------------")
                        self.weight += d["cnt"]
                        self.water += p.water * d["cnt"] * 10
                        self.save()
                    except:
                        print("ошибка работы формы из формсета gen-equipment")
                else:
                    print("for is not valid")

    def getEatChoices(self):
        s = self.eatEnable;
        #   print("ee " + str(self.eatEnable))
        lst = []
        for i in range(4):
            # print(s)
            #  print("i="+str(i)+", mod "+str(2 ** (i + 1)))
            if s % 2 == 1:
                #     print("yes")
                lst.append(i)
            s = s // 2

        return lst


# часть блюда
class RecipePart(models.Model):
    recipe = models.ForeignKey(Recipe)
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

    def generateData(self):
        arr = []
        for ns in self.rParts.all():
            if (ns.recipe != None):
                arr.append({'recipe': str(ns.recipe.pk),
                            'cnt': str(ns.cnt),
                            'eatPart': str(ns.eatPart.pk),
                            'tm': str(ns.tm),

                            })
       # print(arr)
        return arr

    def addFromFormset(self, formset, doCrear=False):
        if (doCrear):
            for ns in self.rParts.all():
                ns.delete()
            self.rParts.clear()

        if formset.is_valid():
            for form in formset.forms:
                if form.is_valid:
                    try:
                        d = form.cleaned_data
                        #print(d)
                        ns = RecipePart.objects.create(recipe=d["recipe"],
                                                       cnt=float(d["cnt"]),
                                                       tm=d["tm"],
                                                       eatPart=d["eatPart"],
                                                       )
                        ns.save()
                        # print(d["cnt"])
                        self.rParts.add(ns)
                        self.save()
                    except:
                        print("ошибка работы формы из формсета gen-equipment")
                else:
                    print("for is not valid")

    def __str__(self):
        return str(self.date)
