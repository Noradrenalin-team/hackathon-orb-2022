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
    path('lk/works', main.lk_works),
    path('lk/work/<int:id>', main.lk_works_work),
    path('lk/result', main.lk_result),
    path('admin/', admin.site.urls),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
