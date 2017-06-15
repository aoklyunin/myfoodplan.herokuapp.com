# -*- coding: utf-8 -*-
from django.core.checks import messages
from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render

from plan.forms import LoginForm, ProductSingleForm, AddProductForm, ProductForm, subdict, RecipeSingleForm, \
    AddRecipeForm, RecipeForm, RecipePortionForm
from plan.models import InfoText, Product, Recipe


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
        'chooseHeader': 'Выберите продукт, который Вы хотите поменять',
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
                S += 2**int(i)
            eq.eatEnable = S
           # print(eq.eatEnable)
            eq.name = form.cleaned_data['name']
            eq.save()
        equipment_formset = RecipePortionFormset(request.POST, request.FILES, prefix='equipment')
        eq.addFromFormset(equipment_formset, True)

  #  print(eq.getEatChoices())
    ef = RecipeForm(instance=eq, prefix="main_form", initial={'eat': eq.getEatChoices()})

    c = {'login_form': LoginForm(),
         'one': '1',
         'pk': eq.pk,
         'form': ef,
         'r':eq,
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


def buy(request):
    c = {
        'pageTitleHeader': 'Главная',
        'login_form': LoginForm(),
        'it': InfoText.objects.get(pageName="constructor_index"),
    }
    return render(request, "constructors/index.html", c)


def plan(request):
    c = {
        'pageTitleHeader': 'Главная',
        'login_form': LoginForm(),
        'it': InfoText.objects.get(pageName="constructor_index"),
    }
    return render(request, "constructors/index.html", c)


'''from django.contrib import messages
from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render

from constructors.form import SchemeForm, EquipmentListForm, EquipmentConstructorSingleForm, AddEquipmentForm, \
    EquipmentSingleWithCtnForm, SchemeSingleForm, EquipmentListWithoutSWForm, EquipmentConstructorForm
from nop.models import Area
from plan.forms import LoginForm, subdict
from plan.models import InfoText
from .models import StockStruct, Equipment, Scheme


# главная страница конструкторского отдела
def index(request):
    c = {
        'area_id': Area.objects.first().pk,
        'login_form': LoginForm(),
        'it': InfoText.objects.get(pageName="constructor_index"),
        'pageTitleHeader': 'Конструкторам',
    }
    return render(request, "constructors/index.html", c)


# баланс на складе
def stockBalance(request, area_id):
    if request.method == "POST":
        # строим форму на основе запроса
        form = EquipmentListForm(request.POST, prefix='main_form')
        # если форма заполнена корректно
        if form.is_valid():
            # получаем объект площадки
            area = Area.objects.get(pk=area_id)
            # формируем список оборудования, у которого есть данные об этой площадке
            lst = []
            for e in form.cleaned_data['equipment']:
                try:
                    eq = Equipment.objects.get(pk=e)
                    flg = True
                    for ss in eq.stockStruct.all():
                        if ss.area == area:
                            lst.append([eq, ss.cnt])
                            flg = False
                    if flg:
                        messages.error(request, "На этой площадке не найдено складской структуры " + eq.name)
                except:
                    messages.error(request, "Оборудования с таким id не найдено")
            # если списокнепустой
            if len(lst) > 0:
                # формируем страницу со списком
                c = {
                    'login_form': LoginForm(),
                    'lst': lst,
                    'area_id': int(area_id),
                    'pageTitleHeader': 'Конструкторам',
                }
                return render(request, "constructors/stockList.html", c)

    c = {
        'area_id': int(area_id),  # иначе не сравнить с id площадки при переборе
        'areas': Area.objects.all().order_by('name'),
        'curPageLink': "/constructors/stock_balance/",
        'login_form': LoginForm(),
        'chooseForm': EquipmentListWithoutSWForm(prefix="main_form"),
        'pageTitleHeader': 'Конструкторам',
        'chooseHeader': 'Выберите оборудование, баланс которого на сладе надо отобразить',
    }
    return render(request, "constructors/stockBalance.html", c)


# страница конструкторской работы
def tehnology(request):
    if request.method == "POST":
        # форма редактирования оборудования
        eq_form = EquipmentConstructorSingleForm(request.POST, prefix='eq_form')
        # если форма заполнена корректно
        if eq_form.is_valid():
            eq = Equipment.objects.get(pk=int(eq_form.cleaned_data['equipment']))
            return HttpResponseRedirect('/constructors/detail/' + str(eq.pk) + '/')
    c = {
        'login_form': LoginForm(),
        'chooseForm': EquipmentConstructorSingleForm(prefix="eq_form"),
        'creationForm': AddEquipmentForm(prefix="main_form"),
        'area_id': Area.objects.first().pk,
        'pageTitleHeader': 'Конструкторам',
        'chooseHeader': 'Выберите оборудование, которое Вы хотите поменять',
        'creationUrl': '/constructors/addEquipment/'
    }
    return render(request, "constructors/tehnology.html", c)


# добавление оборудования
def addEquipment(request):
    if request.method == "POST":
        # форма добавления оборужования
        form = AddEquipmentForm(request.POST, prefix='main_form')
        # если форма заполнена корректно
        if form.is_valid():
            d = {}
            d["name"] = form.cleaned_data["name"]
            d["equipmentType"] = form.cleaned_data["tp"]
            eq = Equipment.objects.create()

            if int(form.cleaned_data["tp"]) == Equipment.TYPE_STANDART_WORK:
                d["dimension"] = "час"
                d["duration"] = 1
            else:
                d["dimension"] = "шт."

            for area in Area.objects.all():
                s = StockStruct.objects.create(area=area)
                eq.stockStruct.add(s)
            eq.save()
            Equipment.objects.filter(pk=eq.pk).update(**d)
            return HttpResponseRedirect('/constructors/detail/' + str(eq.pk) + '/')
    return HttpResponseRedirect('/constructors/work/')


# детализация оборужования
def detailEquipment(request, eq_id):
    EquipmentFormset = formset_factory(EquipmentSingleWithCtnForm)

    eq = Equipment.objects.get(pk=eq_id)

    if request.method == 'POST':
        # строим форму на основе запроса
        form = EquipmentConstructorForm(request.POST, prefix='main_form')
        # если форма заполнена корректно
        if form.is_valid():
            d = subdict(form, ("name", "needVIK", "equipmentType"))
            Equipment.objects.filter(pk=eq_id).update(**d)
            eq = Equipment.objects.get(pk=eq_id)
            if eq.equipmentType == Equipment.TYPE_STANDART_WORK:
                try:
                    eq.duration = form.cleaned_data["duration"]
                except:
                    messages.error("Не получилось задать длительность работы")
            else:
                try:
                    eq.code = form.cleaned_data["code"]
                except:
                    messages.error("Не получилось задать шифр изделия")
            eq.scheme.clear()
            for e in form.cleaned_data["scheme"]:
                eq.scheme.add(e)
            eq.save()
        equipment_formset = EquipmentFormset(request.POST, request.FILES, prefix='equipment')
        eq.addFromFormset(equipment_formset, True)
        gen_formset = EquipmentFormset(request.POST, request.FILES, prefix='gen')
        eq.addGenEquipmentFromFormset(gen_formset, True)

    ef = EquipmentConstructorForm(instance=Equipment.objects.get(pk=eq_id), initial={'scheme': eq.getSchemeChoices()},
                                  prefix="main_form")
    ef.fields["equipmentType"].initial = eq.equipmentType

    #  print(eq.generateDataFromNeedStructs())
    #  print( EquipmentFormset(initial=eq.generateDataFromNeedStructs(), prefix='equipment'))
    c = {'equipment_formset': EquipmentFormset(initial=eq.generateDataFromNeedStructs(), prefix='equipment'),
         'gen_formset': EquipmentFormset(initial=eq.generateDataFromGenEquipment(), prefix='gen'),
         'login_form': LoginForm(),
         'one': '1',
         'form': ef,
         'eqType': eq.equipmentType,
         'tsw': Equipment.TYPE_STANDART_WORK,
         'eq_id': eq_id,
         'area_id': Area.objects.first().pk,
         'formsetNames': ['equipment', 'gen'],
         'pageTitleHeader': 'Конструкторам',
         }
    return render(request, "constructors/detail.html", c)


# удалить конструкторское оборудование
def deleteConstructorEquipment(request, eq_id):
    eq = Equipment.objects.get(pk=eq_id)
    eq.stockStruct.clear()
    eq.delete()
    return HttpResponseRedirect('/constructors/tehnology/')


# список чертежей
def shemes(request):
    if request.method == 'POST':
        # строим форму на основе запроса
        form = SchemeSingleForm(request.POST, prefix="single-scheme")
        # если форма заполнена корректно
        if form.is_valid():
            return HttpResponseRedirect('/constructors/sheme/detail/' + str(form.cleaned_data["scheme"]) + '/')

    return render(request, "constructors/shemesList.html", {
        'login_form': LoginForm(),
        'schs': Scheme.objects.all(),
        'one': '1',
        'addForm': SchemeForm(prefix="add-scheme"),
        'chooseForm': SchemeSingleForm(prefix="single-scheme"),
        'area_id': Area.objects.first().pk,
        'pageTitleHeader': 'Конструкторам',
        'chooseHeader': 'Выберите чертёж, который Вы хотите редактировать',
    })


# Добавить чертеж
def addScheme(request):
    if request.method == "POST":
        # форма добавления оборужования
        form = SchemeForm(request.POST, prefix='add-scheme')
        # если форма заполнена корректно
        if form.is_valid():
            code = form.cleaned_data["code"]
            sch = Scheme.objects.create(link=form.cleaned_data["link"], author=form.cleaned_data["author"])
            sch.save()
            if (code is not None):
                sch.code = code
                sch.save()
            return HttpResponseRedirect('/constructors/sheme/detail/' + str(sch.pk) + '/')
    return HttpResponseRedirect('/constructors/work/')


# Детализация чертежа
def shemeDetail(request, sh_id):
    if request.method == "POST":
        # форма добавления оборужования
        form = SchemeForm(request.POST)
        # если форма заполнена корректно
        if form.is_valid():
            sch = Scheme.objects.get(pk=sh_id)
            code = form.cleaned_data["code"]
            sch.link = form.cleaned_data["link"]
            sch.author = form.cleaned_data["author"]
            if (code is not None):
                sch.code = code
            sch.save()

    return render(request, "constructors/shemesDetail.html", {
        'login_form': LoginForm(),
        'form': SchemeForm(instance=Scheme.objects.get(pk=sh_id)),
        'area_id': Area.objects.first().pk,
        'pageTitleHeader': 'Конструкторам',
    })
'''
