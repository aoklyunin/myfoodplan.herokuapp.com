# -*- coding: utf-8 -*-
# обработчик адресов сайта
from django.conf.urls import include, url
from django.contrib import admin

import plan.views
import plan.auth

# автоопределение администратора
admin.autodiscover()

urlpatterns = [
    # панель администратора
    url(r'^admin/', include(admin.site.urls)),
    # выход из сайта
    url(r'^logout/$', plan.auth.logout_view),
    # регистрация на сайте
    url(r'^register/$', plan.auth.register),
    url(r'^products/$', plan.views.products),
    url(r'^product/add/$', plan.views.addProduct),
    url(r'^product/detail/(?P<product_id>[0-9]+)/$$', plan.views.detailProduct),
    url(r'^product/delete/(?P<product_id>[0-9]+)/$$', plan.views.deleteProduct),
    url(r'^recipe/add/$', plan.views.addRecipe),
    url(r'^recipe/detail/(?P<recipe_id>[0-9]+)/$$', plan.views.detailRecipe),
    url(r'^recipe/delete/(?P<recipe_id>[0-9]+)/$$', plan.views.deleteRecipe),
    url(r'^recipes/$', plan.views.recipes),
    url(r'^plan/add/$', plan.views.addPlan),
    url(r'^plan/detail/(?P<plan_id>[0-9]+)/$$', plan.views.detailPlan),
    url(r'^plan/delete/(?P<plan_id>[0-9]+)/$$', plan.views.deletePlan),
    url(r'^plans/$', plan.views.plans),
    url(r'^login/$', plan.auth.login),
    url(r'^buy/$', plan.views.buy),
    url(r'^balance/$', plan.views.balance),
    url(r'^', plan.views.index, name='index'),
]
