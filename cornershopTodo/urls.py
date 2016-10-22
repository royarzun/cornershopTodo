# coding=utf-8

from django.conf.urls import url, include

from rest_framework.authtoken import views
from rest_framework.urlpatterns import format_suffix_patterns

from todo.views import RegistroView, TareasView, TareaView


urlpatterns = [
    url(r'^api-token/?$', views.obtain_auth_token),
    url(r'^docs/?', include('rest_framework_swagger.urls')),
    url(r'^registro/?$', RegistroView.as_view()),
    url(r'^tareas/?$', TareasView.as_view()),
    url(r'^tareas/(?P<tarea_id>[0-9]*)/?$', TareaView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
