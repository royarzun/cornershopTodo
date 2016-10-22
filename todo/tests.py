# coding=utf-8

from rest_framework import status
from rest_framework.test import APITestCase


class RegistroAPITestCase(APITestCase):

    dummy_user = {"username": "el_usuario", "password": "la_password"}
    dummy_user_uno = {"username": "el_usuario1", "password": "la_password"}
    dummy_user_dos = {"username": "el_usuario2", "password": "la_password"}

    def test_registro_usuario(self):
        """ Dado que un usuario nuevo se registra, debemos obtener status
        201, en el response al request.

        PS: esto es una decision arbitraria por simplicidad, por supuesto pudo
        haber sido cualquier otro response.
        """
        response = self.client.post("/registro/", self.dummy_user,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_registro_usuario_ya_registrado(self):
        """ Dado que intentamos registrar un usuario dos veces, la segunda vez
        que se hace el request deberia retornar status 400.'
        """
        response = self.client.post("/registro/", self.dummy_user_uno,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post("/registro/", self.dummy_user_uno,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_obtener_token_usuario_registrado(self):
        self.client.post("/registro/", self.dummy_user, format="json")
        response = self.client.post("/api-token/", self.dummy_user, format="json")
        # probar que el key 'token' se encuentra en el response
        self.assertTrue("token" in response.data)
        # probar tamaño valido del token
        self.assertEqual(len(response.data["token"]), 40)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_obtener_token_usuario_no_registrado(self):
        response = self.client.post("/api-token/", self.dummy_user_dos, format="json")
        # probar que el key 'token' se encuentra en el response
        self.assertFalse("token" in response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TareasAPITestCase(APITestCase):
    usuario_dummy = {"username": "royarzun", "password": "foo"}
    tarea_dummy = {"titulo": "tituloFoo", "descripcion": "foo"}

    def get_token(self):
        self.client.post('/registro/', self.usuario_dummy, format="json")
        response = self.client.post('/api-token/', self.usuario_dummy,
                                    format="json")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' +
                                                   response.data["token"])

    def test_crear_una_tarea_para_usuario_registrado(self):
        self.get_token()
        response = self.client.post("/tareas/", self.tarea_dummy, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # probar que se puede obtener de vuelta
        response = self.client.get("/tareas/")
        self.assertEqual(len(response.data), 1)

    def test_crear_tarea_con_datos_invalidos(self):
        self.get_token()
        response = self.client.post("/tareas/", {"titulo": 1}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
