# coding=utf-8

from django.conf.urls import url
from django.contrib import admin

from rest_framework.urlpatterns import format_suffix_patterns

from todo.views import RegistroView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^registro/', RegistroView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
