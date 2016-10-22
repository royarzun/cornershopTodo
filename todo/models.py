# coding=utf-8

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class TodoTarea(models.Model):
    """ Clase TodoTarea

    Esta clase es la que estara a cargo de registrar las tareas en la lista TODO

    Attributes:
        asignado (User): Usuario asignado a la tarea
        titulo (String): Titulo de la tarea
        descripcion (String): Descripcion de la tarea
        realizada (boolean): Estado de completado de la tarea
        ultima_actualizacion (DateTime): Ultima vez que se edito en la BD
    """
    asignado = models.ForeignKey(User)
    titulo = models.CharField(max_length=35, blank=False)
    descripcion = models.TextField(max_length=100, blank=False)
    realizada = models.BooleanField(default=False)
    ultima_actualizacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s:%s" % (str(self.asignado), self.descripcion)
