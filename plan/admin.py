# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.
from plan.models import ProductType, Product, ProductPortion, Recipe, EatPart, DailyPlan, RecipePart, RemainPortion, \
    InfoText, RecipeType

admin.site.register(ProductType)
admin.site.register(Product)
admin.site.register(ProductPortion)
admin.site.register(Recipe)
admin.site.register(EatPart)
admin.site.register(RecipePart)
admin.site.register(DailyPlan)
admin.site.register(RemainPortion)
admin.site.register(InfoText)
admin.site.register(RecipeType)