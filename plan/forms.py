# -*- coding: utf-8 -*-
# модуль с формами
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from django import forms
import datetime
# форма логина
from django.db.models import BLANK_CHOICE_DASH
from django.forms import Form, CharField, TextInput, ChoiceField, ModelChoiceField, ModelForm, FloatField, DateField, \
    Textarea, IntegerField

from plan.models import Product, ProductType, Recipe, DailyPlan, RecipePart, EatPart, RecipeType


def subdict(form, keyset):
    return dict((k, form.cleaned_data[k]) for k in keyset)


# получить список оборудования
def getProducts():
    equipments = []
    for i in ProductType.objects.all().order_by('name'):
        lst = []
        for eq in Product.objects.filter(tp=i).order_by('name'):
            lst.append([eq.id, str(eq)])
        equipments.append([i.name, lst])

    return equipments + BLANK_CHOICE_DASH


# получить список оборудования
def getPlans():
    equipments = []
    for i in DailyPlan.objects.all().order_by('-date'):
        equipments.append([i.pk, i])

    return equipments + BLANK_CHOICE_DASH


# получить список оборудования
def getRecipes():
    equipments = []
    for i in RecipeType.objects.all().order_by('name'):
        lst = []
        for eq in Recipe.objects.filter(tp=i).order_by('name'):
            lst.append([eq.id, str(eq)])
        equipments.append([i.name, lst])

    return equipments + BLANK_CHOICE_DASH


class LoginForm(forms.Form):
    # имя пользователя
    username = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 20, 'placeholder': 'Логин'}),
                               label="")
    # пароль
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}), label="")

    widgets = {
        'password': forms.PasswordInput(),
    }


# форма регистрации
class RegisterForm(forms.Form):
    # логин
    username = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 20, 'placeholder': 'mylogin'}),
                               label="Логин")
    # пароль
    password = forms.CharField(widget=forms.PasswordInput(attrs={'rows': 1, 'cols': 20, 'placeholder': 'qwerty123'}),
                               label="Пароль")
    # повтор пароля
    rep_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'rows': 1, 'cols': 20, 'placeholder': 'qwerty123'}),
        label="Повторите пароль")
    # почта
    mail = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 20, 'placeholder': 'example@gmail.com'}),
                           label="Адрес электронной почты")
    # имя
    name = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 20, 'placeholder': 'Иван'}), label="Имя")
    # фамилия
    second_name = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 20, 'placeholder': 'Иванов'}),
                                  label="Фамилия")


# форма для добавления новых изделий
class AddProductForm(Form):
    name = CharField(max_length=10000, label="Название",
                     widget=TextInput(attrs={'placeholder': 'Огурец'}))
    tp = ModelChoiceField(label="Тип", queryset=ProductType.objects.all().order_by('name'))

    def __init__(self, *args, **kwargs):
        super(AddProductForm, self).__init__(*args, **kwargs)


# форма для выбора изделия для редактирования  конструктором
class ProductSingleForm(Form):
    equipment = ChoiceField(label="")

    def __init__(self, *args, **kwargs):
        super(ProductSingleForm, self).__init__(*args, **kwargs)
        self.fields['equipment'].choices = getProducts()
        self.fields['equipment'].widget.attrs['class'] = 'beautiful-select'
        self.fields['equipment'].widget.attrs['id'] = 'equipment'


# форма оборудования
class ProductForm(ModelForm):
    cf = ChoiceField(label="Ёмкость по умолчанию")

    class Meta:
        model = Product
        fields = {'name', 'proteins', 'fats', 'carbohydrates', 'caloricity', 'tp', 'cnt', 'dt', 'water',
                  'remain', 'inSmallSpoon', 'inBigSpoon', 'inUnit', 'density', 'inGlass'}
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Изделие'}),
        }

        labels = {
            'name': 'Название',
            'proteins': 'Белки',
            'fats': 'Жиры',
            'carbohydrates': 'Углеводы',
            'caloricity': 'Калорийность',
            'tp': 'Тип',
            'cnt': 'Кол-во в упаковке',
            'dt': 'срок годности',
            'water': 'воды мл.',
            'remain': 'остаток',
            'inSmallSpoon': 'в чайной ложке',
            'inBigSpoon': 'в столовой ложке',
            'inUnit': 'вес штуки',
            'density': 'плотность',
            'inGlass': 'в стакане',
        }

        error_messages = {
            'name': {'invalid': '', 'invalid_choice': ''},
            'duration': {'required': ''},
        }

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['cf'].choices = Product.capacityChoices


# форма для выбора изделия для редактирования  конструктором
class RecipeSingleForm(Form):
    equipment = ChoiceField(label="")

    def __init__(self, *args, **kwargs):
        super(RecipeSingleForm, self).__init__(*args, **kwargs)
        self.fields['equipment'].choices = getRecipes()
        self.fields['equipment'].widget.attrs['class'] = 'beautiful-select'
        self.fields['equipment'].widget.attrs['id'] = 'equipment'


# форма оборудования
class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = {'name', 'instruction', 'remain', 'eatParts', 'tp', 'portionCnt'}
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Изделие'}),
            'instruction': forms.Textarea(attrs={'cols': 80, 'rows': 10}),
        }

        labels = {
            'name': 'Название',
            'instruction': 'Инструкция',
            'remain': 'Остаток',
            'eatParts': 'Приёмы пищи',
            'tp': 'тип',
            'portionCnt': 'кол-во порций',
        }

        error_messages = {
            'name': {'invalid': '', 'invalid_choice': ''},
        }

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(RecipeForm, self).__init__(*args, **kwargs)
        self.fields['instruction'].required = False


# форма для добавления новых изделий
class AddRecipeForm(Form):
    name = CharField(max_length=10000, label="Название",
                     widget=TextInput(attrs={'placeholder': 'Рагу'}))

    tp = ModelChoiceField(label="Тип", queryset=RecipeType.objects.all())

    def __init__(self, *args, **kwargs):
        super(AddRecipeForm, self).__init__(*args, **kwargs)


# форма для выбора одного изделия с кол-вом
class RecipePortionForm(Form):
    product = ChoiceField(label="")
    weight = FloatField(label="")
    cnt = FloatField(label="")

    def __init__(self, *args, **kwargs):
        super(RecipePortionForm, self).__init__(*args, **kwargs)
        self.fields['product'].choices = getProducts()
        self.fields['product'].widget.attrs['class'] = 'beautiful-select'
        self.fields['product'].widget.attrs['id'] = 'equipment'

        self.fields['product'].initial = None
        self.fields['weight'].initial = 0
        self.fields['cnt'].initial = 0
        self.fields['product'].required = False
        self.fields['weight'].required = False
        self.fields['cnt'].required = False


# форма для добавления новых изделий
class AddDailyPlanForm(Form):
    date = DateField(label="Дата")

    def __init__(self, *args, **kwargs):
        super(AddDailyPlanForm, self).__init__(*args, **kwargs)
        self.fields['date'].widget.attrs['id'] = 'datepicker'


class DailyPlanSingleForm(Form):
    equipment = ChoiceField(label="")

    def __init__(self, *args, **kwargs):
        super(DailyPlanSingleForm, self).__init__(*args, **kwargs)
        self.fields['equipment'].choices = getPlans()
        self.fields['equipment'].widget.attrs['class'] = 'beautiful-select'
        self.fields['equipment'].widget.attrs['id'] = 'equipment'


# форма оборудования
class RecipePartForm(ModelForm):
    class Meta:
        model = RecipePart
        fields = {'cnt', 'eatPart', 'tm', 'recipe'}
        widgets = {

        }

        labels = {
            'cnt': '',
            'eatPart': '',
            'tm': '',
            'recipe': '',
        }

        error_messages = {
            'name': {'invalid': '', 'invalid_choice': ''},
        }

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(RecipePartForm, self).__init__(*args, **kwargs)
        self.fields['eatPart'].required = False
        self.fields['tm'].widget = forms.TimeInput(format='%H:%M')
        self.fields['tm'].widget.attrs['class'] = 'timepicker123'


class RecipeAdminModelForm(ModelForm):
    class Meta:
        model = Recipe
        widgets = {
            'instruction': Textarea(attrs={'cols': 100, 'rows': 10}),
        }
        fields = '__all__'
