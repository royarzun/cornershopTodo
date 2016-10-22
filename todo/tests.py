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
        """ Dado que el usuario se encuentra registrado, se prueba la efectiva
        obtencion de su token.
        """
        self.client.post("/registro/", self.dummy_user, format="json")
        response = self.client.post("/api-token/", self.dummy_user, format="json")
        # probar que el key 'token' se encuentra en el response
        self.assertTrue("token" in response.data)
        # probar tamaño valido del token
        self.assertEqual(len(response.data["token"]), 40)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_obtener_token_usuario_no_registrado(self):
        """ Dado que se intenta usar malas credenciales de usuario para obtener
        un token, el response debe ser status=400 como BAD REQUEST
        """
        response = self.client.post("/api-token/", self.dummy_user_dos, format="json")
        # probar que el key 'token' se encuentra en el response
        self.assertFalse("token" in response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TareasAPITestCase(APITestCase):

    usuario_dummy = {"username": "pepe", "password": "jojojo"}
    tarea_dummy = {"titulo": "tituloFoo", "descripcion": "foo"}

    fixtures = ['fixtures.json']

    def get_token(self):
        """Helper para obtener token. """
        self.client.post('/registro/', self.usuario_dummy, format="json")
        response = self.client.post('/api-token/', self.usuario_dummy,
                                    format="json")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' +
                                                   response.data["token"])

    def test_crear_una_tarea_para_usuario_registrado(self):
        """ Dado que un usuario esta registrado, se testea el crear una tarea
        con input valido"""
        self.get_token()
        response = self.client.post("/tareas/", self.tarea_dummy, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # probar que se puede obtener de vuelta
        id = response.data
        response = self.client.get("/tareas/"+ str(id))
        self.assertEqual(response.data["id"], id)

    def test_actualizar_tarea_id_valido(self):
        """ Dado que tengo una tarea en la BD, deberia ser capaz de actualizar
        una tarea sin necesariamente tener que cambiar el estado"""
        modifificacion = {"descripcion": "Hacer sandwiches"}
        self.get_token()
        response = self.client.put("/tareas/2", modifificacion, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get("/tareas/2")
        self.assertEqual(response.data["descripcion"], "Hacer sandwiches")

    def test_actualizar_tarea_id_invalido(self):
        """ Dado que tengo una tarea en la BD, deberia ser capaz de actualizar
        una tarea sin necesariamente tener que cambiar el estado"""
        modifificacion = {"descripcion": "Hacer sandwiches"}
        self.get_token()
        response = self.client.put("/tareas/22", modifificacion, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_actualizar_tarea_colocando_atributo_tarea_realizada(self):
        """ Dado que tengo una tarea en la BD, deberia ser capaz de actualizar
        una tarea a 'realizada' solo usando la id, siendo los demas atributos
        opcionales"""
        self.get_token()
        modifificacion = {"realizada": True}
        response = self.client.put("/tareas/2", modifificacion, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get("/tareas/2")
        self.assertTrue(response.data["realizada"])
