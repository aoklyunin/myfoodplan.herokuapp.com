# -*- coding: utf-8 -*-
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render

from plan.forms import RegisterForm, LoginForm


# метод регистрации
def register(request):
    # если post запрос
    if request.method == 'POST':
        # строим форму на основе запроса
        form = RegisterForm(request.POST)
        # если форма заполнена корректно
        if form.is_valid():
            # проверяем, что пароли совпадают
            if form.cleaned_data["password"] != form.cleaned_data["rep_password"]:
                # выводим сообщение и перезаполняем форму
                messages.error(request, "пароли не совпадают")
                data = {'username': form.cleaned_data["username"],

                        'mail': form.cleaned_data["mail"],
                        'name': form.cleaned_data["name"],
                        'second_name': form.cleaned_data["second_name"],
                        }
                # перерисовываем окно
                return render(request, "plan/register.html", {
                    'form': RegisterForm(initial=data),
                    'ins_form': LoginForm()
                })
            else:
                # получаем данные из формы
                musername = form.cleaned_data["username"]

                mmail = form.cleaned_data["mail"]
                name = form.cleaned_data["name"]
                second_name = form.cleaned_data["second_name"]
                mpassword = form.cleaned_data["password"]
                try:
                    # создаём пользователя
                    user = User.objects.create_user(username=musername,
                                                    email=mmail,
                                                    password=mpassword)
                    # если получилось создать пользователя
                    if user:
                        # задаём ему имя и фамилию
                        user.first_name = name
                        user.last_name = second_name
                        # созраняем пользователя
                        user.save()
                    return HttpResponseRedirect("/")
                except:
                    # если не получилось создать пользователя, то выводим сообщение
                    messages.error(request, "Такой пользователь уже есть")
                    # заполняем дату формы
                    data = {'username': form.cleaned_data["username"],
                            'mail': form.cleaned_data["mail"],
                            'name': form.cleaned_data["name"],
                            'second_name': form.cleaned_data["second_name"],
                            }
                    # рисуем окно регистрации
                    return render(request, "plan/register.html", {
                        'form': RegisterForm(initial=data),
                        'ins_form': LoginForm()
                    })
        else:
            # перезагружаем страницу
            return HttpResponseRedirect("/")
    else:
        # возвращаем простое окно регистрации
        return render(request, "plan/register.html", {
            'form': RegisterForm(),
            'login_form': LoginForm()
        })


# выход из системы
def logout_view(request):
    logout(request)
    return HttpResponseRedirect("../../../../")



# стартовая страница
def login(request):
    # обработка входа
    if request.method == "POST":
        # если в post-запросе есть поля логина/пароля
        if ("username" in request.POST) and ("password" in request.POST):
            username = request.POST['username']
            password = request.POST['password']
            # пробуем залогиниться
            user = auth.authenticate(username=username, password=password)
            request.POST._mutable = True
            # если полльзователь существует и он активен
            if user is not None and user.is_active:
                # входим на сайт
                auth.login(request, user)
                # выводим сообщение об удаче
                messages.success(request, "успешный вход")
            else:
                messages.error(request, "пара логин-пароль не найдена")

    return HttpResponseRedirect("../../../../")
