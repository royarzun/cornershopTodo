# coding=utf-8

from django.contrib.auth.models import User

from rest_framework import serializers

from todo.models import TodoTarea


class RegistroSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password")


class TareasSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoTarea
        fields = ("asignado", "titulo", "descripcion", "realizada")
