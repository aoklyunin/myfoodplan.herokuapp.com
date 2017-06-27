# -*- coding: utf-8 -*-
# модуль с формами
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from django import forms
import datetime
# форма логина
from django.db.models import BLANK_CHOICE_DASH
from django.forms import Form, CharField, TextInput, ChoiceField, ModelChoiceField, ModelForm, FloatField, DateField

from plan.models import Product, ProductType, Recipe, DailyPlan, RecipePart


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
    for i in Recipe.objects.all().order_by('name'):
        equipments.append([i.pk, i])

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
    class Meta:
        model = Product
        fields = {'dimention', 'name', 'proteins', 'fats', 'carbohydrates', 'caloricity', 'tp', 'cnt', 'dt', 'water',
                  'remain'}
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Изделие'}),
        }

        labels = {
            'name': 'Название',
            'dimention': 'Единица измерения',
            'proteins': 'Белки',
            'fats': 'Жиры',
            'carbohydrates': 'Углеводы',
            'caloricity': 'Калорийность',
            'tp': 'Тип',
            'cnt': 'Кол-во в упаковке',
            'dt': 'срок годности',
            'water': 'воды мл.',
            'remain': 'остаток'
        }

        error_messages = {
            'name': {'invalid': '', 'invalid_choice': ''},
            'duration': {'required': ''},
        }

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(ProductForm, self).__init__(*args, **kwargs)


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
    eat = forms.MultipleChoiceField(
        choices=(
            (0, 'завтрак'),
            (1, 'обед'),
            (2, 'полдник'),
            (3, 'ужин'),
        ),
        label="Когда можно есть", required=False)

    class Meta:
        model = Recipe
        fields = {'name', 'instruction', 'remain'}
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Изделие'}),
            'instruction': forms.Textarea(attrs={'cols': 80, 'rows': 10}),
        }

        labels = {
            'name': 'Название',
            'instruction': 'Инструкция',
            'remain': 'Остаток',

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

    def __init__(self, *args, **kwargs):
        super(AddRecipeForm, self).__init__(*args, **kwargs)


# форма для выбора одного изделия с кол-вом
class RecipePortionForm(Form):
    product = ChoiceField(label="")
    cnt = FloatField(label="")

    def __init__(self, *args, **kwargs):
        super(RecipePortionForm, self).__init__(*args, **kwargs)
        self.fields['product'].choices = getProducts()
        self.fields['product'].widget.attrs['class'] = 'beautiful-select'
        self.fields['product'].widget.attrs['id'] = 'equipment'

        self.fields['product'].initial = None
        self.fields['cnt'].initial = 0
        self.fields['product'].required = False
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
        fields = {'cnt', 'eatPart', 'tm','recipe'}
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

