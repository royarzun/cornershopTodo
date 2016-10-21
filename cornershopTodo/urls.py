# coding=utf-8

from django.conf.urls import url

from rest_framework.authtoken import views
from rest_framework.urlpatterns import format_suffix_patterns

from todo.views import RegistroView


urlpatterns = [
    url(r'^registro/?$', RegistroView.as_view()),
    url(r'^api-token/?$', views.obtain_auth_token),
]

urlpatterns = format_suffix_patterns(urlpatterns)
