# coding=utf-8

from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase


class RegistroAPITestCase(APITestCase):

    dummy_user = {"username": "el_usuario", "password": "la_password"}

    def test_registro_usuario(self):
        response = self.client.post("/registro/", self.dummy_user,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)