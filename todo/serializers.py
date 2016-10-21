# coding=utf-8

from django.contrib.auth.models import User

from rest_framework import serializers


class RegistroSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password")
