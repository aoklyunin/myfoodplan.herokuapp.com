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
    url(r'^recipes/$', plan.views.recipes),
    url(r'^plan/$', plan.views.plan),
    url(r'^buy/$', plan.views.buy),
    url(r'^', plan.views.index, name='index'),
]
