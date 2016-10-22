# coding=utf-8

from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from todo.models import TodoTarea


class RegistroSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password")
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('username', 'password')
            )
        ]
