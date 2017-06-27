# -*- coding: utf-8 -*-
import datetime

from django.core.checks import messages
from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render

from plan.forms import LoginForm, ProductSingleForm, AddProductForm, ProductForm, subdict, RecipeSingleForm, \
    AddRecipeForm, RecipeForm, RecipePortionForm, DailyPlanSingleForm, AddDailyPlanForm, RecipePartForm
from plan.models import InfoText, Product, Recipe, DailyPlan


# главная страница
def index(request):
    c = {
        'pageTitleHeader': 'Главная',
        'login_form': LoginForm(),
        'it': InfoText.objects.get(pageName="plan_index"),
    }
    return render(request, "plan/index.html", c)


# продукты
def products(request):
    if request.method == "POST":
        # форма редактирования оборудования
        eq_form = ProductSingleForm(request.POST, prefix='eq_form')
        # если форма заполнена корректно
        if eq_form.is_valid():
            eq = Product.objects.get(pk=int(eq_form.cleaned_data['equipment']))
            return HttpResponseRedirect('/product/detail/' + str(eq.pk) + '/')

    c = {
        'chooseForm': ProductSingleForm(prefix="eq_form"),
        'addForm': AddProductForm(prefix="main_form"),
        'pageTitleHeader': 'Продукты',
        'chooseHeader': 'Выберите продукт, который Вы хотите поменять',
        'creationUrl': '/constructors/addEquipment/'
    }
    return render(request, "plan/products.html", c)


# добавить продукт
def addProduct(request):
    if request.method == "POST":
        # форма добавления оборужования
        form = AddProductForm(request.POST, prefix='main_form')
        # если форма заполнена корректно
        if form.is_valid():
            d = {}
            d["name"] = form.cleaned_data["name"]
            d["tp"] = form.cleaned_data["tp"]
            eq = Product.objects.create(**d)
            eq.save()
            return HttpResponseRedirect('/product/detail/' + str(eq.pk) + '/')
    return HttpResponseRedirect('/products/')


# детализация продуктов
def detailProduct(request, product_id):
    eq = Product.objects.get(pk=product_id)
    if request.method == 'POST':
        # строим форму на основе запроса
        form = ProductForm(request.POST, prefix='main_form')
        # если форма заполнена корректно
        if form.is_valid():
            eq.dimention = form.cleaned_data['dimention']
            eq.name = form.cleaned_data['name']
            eq.proteins = form.cleaned_data['proteins']
            eq.fats = form.cleaned_data['fats']
            eq.carbohydrates = form.cleaned_data['carbohydrates']
            eq.caloricity = form.cleaned_data['caloricity']
            eq.cnt = form.cleaned_data['cnt']
            eq.dt = form.cleaned_data['dt']
            eq.water = form.cleaned_data['water']
            eq.tp = form.cleaned_data["tp"]
            eq.remain = form.cleaned_data["remain"]
            eq.save()

    ef = ProductForm(instance=eq, prefix="main_form")

    c = {'login_form': LoginForm(),
         'one': '1',
         'pk': eq.pk,
         'form': ef,
         'pageTitleHeader': 'Продукт',
         }
    return render(request, "plan/detailProduct.html", c)


# удалить продукт
def deleteProduct(request, product_id):
    eq = Product.objects.get(pk=product_id)
    eq.delete()
    return HttpResponseRedirect('/products/')


# продукты
def recipes(request):
    if request.method == "POST":
        # форма редактирования оборудования
        eq_form = RecipeSingleForm(request.POST, prefix='eq_form')
        # если форма заполнена корректно
        if eq_form.is_valid():
            eq = Recipe.objects.get(pk=int(eq_form.cleaned_data['equipment']))
            return HttpResponseRedirect('/recipe/detail/' + str(eq.pk) + '/')

    c = {
        'chooseForm': RecipeSingleForm(prefix="eq_form"),
        'addForm': AddRecipeForm(prefix="main_form"),
        'pageTitleHeader': 'Рецепты',
        'chooseHeader': 'Выберите рецепт, который Вы хотите поменять',
        'chooseLabel': 'Выбрать рецепт',
        'creationUrl': '/recipe/add/'
    }
    return render(request, "plan/recipes.html", c)


# добавить продукт
def addRecipe(request):
    if request.method == "POST":
        # форма добавления оборужования
        form = AddRecipeForm(request.POST, prefix='main_form')
        # если форма заполнена корректно
        if form.is_valid():
            d = {}
            d["name"] = form.cleaned_data["name"]
            eq = Recipe.objects.create(**d)
            eq.save()
            return HttpResponseRedirect('/recipe/detail/' + str(eq.pk) + '/')
    return HttpResponseRedirect('/recipes/')


# детализация продуктов
def detailRecipe(request, recipe_id):
    RecipePortionFormset = formset_factory(RecipePortionForm)
    eq = Recipe.objects.get(pk=recipe_id)
    if request.method == 'POST':
        # строим форму на основе запроса
        form = RecipeForm(request.POST, prefix='main_form')
        # если форма заполнена корректно
        if form.is_valid():
            eq.instruction = form.cleaned_data['instruction']
            S = 0
            for i in form.cleaned_data['eat']:
                S += 2 ** int(i)
            eq.eatEnable = S
            # print(eq.eatEnable)
            eq.name = form.cleaned_data['name']
            eq.remain = form.cleaned_data["remain"]
            eq.portionCnt = form.cleaned_data["portionCnt"]
            eq.save()
        equipment_formset = RecipePortionFormset(request.POST, request.FILES, prefix='equipment')
        eq.addFromFormset(equipment_formset, True)

        #  print(eq.getEatChoices())
    ef = RecipeForm(instance=eq, prefix="main_form", initial={'eat': eq.getEatChoices()})

    c = {'login_form': LoginForm(),
         'one': '1',
         'pk': eq.pk,
         'form': ef,
         'r': eq,
         'formsetNames': ['equipment'],
         'pageTitleHeader': 'Рецепты',
         'equipment_formset': RecipePortionFormset(initial=eq.generateData(), prefix='equipment')
         }
    return render(request, "plan/detailRecipe.html", c)


# удалить продукт
def deleteRecipe(request, recipe_id):
    eq = Recipe.objects.get(pk=recipe_id)
    eq.delete()
    return HttpResponseRedirect('/recipes/')


def plans(request):
    if request.method == "POST":
        # форма редактирования оборудования
        eq_form = DailyPlanSingleForm(request.POST, prefix='eq_form')
        # если форма заполнена корректно
        if eq_form.is_valid():
            eq = Product.objects.get(pk=int(eq_form.cleaned_data['equipment']))
            return HttpResponseRedirect('/plan/detail/' + str(eq.pk) + '/')

    c = {
        'chooseForm': DailyPlanSingleForm(prefix="eq_form"),
        'addForm': AddDailyPlanForm(prefix="main_form", initial={'date': datetime.date.today}),
        'pageTitleHeader': 'Примы пищи',
        'chooseHeader': 'Выберите приём пищи, который Вы хотите поменять',
        'creationUrl': '/plan/add/',
        'chooseLabel': 'Выбрать день',
    }
    return render(request, "plan/plans.html", c)


# добавить продукт
def addPlan(request):
    if request.method == "POST":
        # форма добавления оборужования
        form = AddDailyPlanForm(request.POST, prefix='main_form')
        # если форма заполнена корректно
        if form.is_valid():
            d = {}
            d["date"] = form.cleaned_data["date"]
            eq = DailyPlan.objects.create(**d)
            eq.save()
            return HttpResponseRedirect('/plan/detail/' + str(eq.pk) + '/')
    return HttpResponseRedirect('/plans/')


# детализация продуктов
def detailPlan(request, plan_id):
    RecipePortionFormset = formset_factory(RecipePartForm)
    eq = DailyPlan.objects.get(pk=plan_id)
    if request.method == 'POST':
        # строим форму на основе запроса
        form = AddDailyPlanForm(request.POST, prefix='main_form')
        # если форма заполнена корректно
        if form.is_valid():
            eq.date = form.cleaned_data['date']
            eq.save()
        equipment_formset = RecipePortionFormset(request.POST, request.FILES, prefix='equipment')
        eq.addFromFormset(equipment_formset, True)

        #  print(eq.getEatChoices())
    ef = AddDailyPlanForm(initial={'date': eq.date}, prefix="main_form")

    c = {'login_form': LoginForm(),
         'one': '1',
         'pk': eq.pk,
         'form': ef,
         'r': eq,
         'formsetNames': ['equipment'],
         'pageTitleHeader': 'Рецепты',
         'equipment_formset': RecipePortionFormset(initial=eq.generateData(), prefix='equipment')
         }
    return render(request, "plan/detailPlan.html", c)


# удалить продукт
def deletePlan(request, plan_id):
    eq = DailyPlan.objects.get(pk=plan_id)
    eq.delete()
    return HttpResponseRedirect('/recipes/')


def buy(request):
    c = {
        'pageTitleHeader': 'Главная',
        'login_form': LoginForm(),
        'it': InfoText.objects.get(pageName="constructor_index"),
    }
    return render(request, "constructors/index.html", c)


def balance(request):
    c = {
        'pageTitleHeader': 'Главная',
        'login_form': LoginForm(),
        'it': InfoText.objects.get(pageName="constructor_index"),
    }
    return render(request, "constructors/index.html", c)
