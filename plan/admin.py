# -*- coding: utf-8 -*-
from django import forms
from django.contrib import admin

# Register your models here.
from django.db import models
from django.forms import Textarea

from plan.forms import RecipeAdminModelForm
from plan.models import ProductType, Product, ProductPortion, Recipe, EatPart, DailyPlan, RecipePart, RemainPortion, \
    InfoText, RecipeType


class RecipeAdmin(admin.ModelAdmin):
    form = RecipeAdminModelForm


admin.site.register(ProductType)
admin.site.register(Product)
admin.site.register(ProductPortion)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(EatPart)
admin.site.register(RecipePart)
admin.site.register(DailyPlan)
admin.site.register(RemainPortion)
admin.site.register(InfoText)
admin.site.register(RecipeType)
