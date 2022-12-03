from django.contrib import admin
from django.urls import path

import main.views as main
import lk.views as lk

urlpatterns = [
    path('', main.index),
    path('registration', main.index),
    path('work/<int:id>', main.index),
    path('login', lk.login),
    path('logout', lk.login),
    path('lk', lk.login),
    path('lk/work', lk.login),
    path('lk/applications', lk.login),
    path('lk/application/<int:id>', lk.login),
    path('lk/experts', lk.login),
    path('lk/expert/add', lk.login),
    path('lk/expert/<int:id>', lk.login),
    path('lk/info', lk.login),
    path('lk/works', lk.login),
    path('lk/work/<int:id>', lk.login),
]
