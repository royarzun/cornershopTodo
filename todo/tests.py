# coding=utf-8

from rest_framework import status
from rest_framework.test import APITestCase


class RegistroAPITestCase(APITestCase):

    dummy_user = {"username": "el_usuario", "password": "la_password"}
    dummy_user_uno = {"username": "el_usuario1", "password": "la_password"}

    def test_registro_usuario(self):
        """ Dado que un usuario nuevo se registra, debemos obtener status
        201, en el response al request.

        PS: esto es una decision arbitraria por simplicidad, por supuesto pudo
        haber sido cualquier otro response.
        """
        response = self.client.post("/registro/", self.dummy_user,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_obtener_token_usuario_registrado(self):
        self.client.post("/registro/", self.dummy_user, format="json")
        response = self.client.post("/api-token/", self.dummy_user, format="json")
        self.assertTrue("token" in response.data)
        self.assertEqual(len(response.data["token"]), 40)
    def test_registro_usuario_ya_registrado(self):
        """ Dado que intentamos registrar un usuario dos veces, la segunda vez
        que se hace el request deberia retornar status 400. Este codigo ha sido
        elegido por el validador del serializador de Registro en
        'todo.serializers.RegistroSerializer'
        """
        response = self.client.post("/registro/", self.dummy_user_uno,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post("/registro/", self.dummy_user_uno,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
