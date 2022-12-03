from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings


import main.views as main
import lk.views as lk

urlpatterns = [
    path('', main.index),
    path('registration', main.registration),
    path('work/<int:id>', main.work),
    path('login', main.login),
    path('logout', main.logout),
    path('lk', main.lk),
    path('lk/work', main.lk_work),
    path('lk/applications', lk.login),
    path('lk/application/<int:id>', lk.login),
    path('lk/experts', lk.login),
    path('lk/expert/add', lk.login),
    path('lk/expert/<int:id>', lk.login),
    path('lk/info', lk.login),
    path('lk/works', lk.login),
    path('lk/work/<int:id>', lk.login),
    path('admin/', admin.site.urls),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
