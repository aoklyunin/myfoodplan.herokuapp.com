# -*- coding: utf-8 -*-
# модуль с формами
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from django import forms

# форма логина
from django.db.models import BLANK_CHOICE_DASH
from django.forms import Form, CharField, TextInput, ChoiceField, ModelChoiceField, ModelForm

from plan.models import Product, ProductType


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
        fields = {'dimention', 'name', 'proteins', 'fats', 'carbohydrates', 'caloricity', 'tp', 'cnt', 'dt', 'water'}
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
            'water': 'воды мл.'
        }

        error_messages = {
            'name': {'invalid': '', 'invalid_choice': ''},
            'duration': {'required': ''},
        }

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(ProductForm, self).__init__(*args, **kwargs)
