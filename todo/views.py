# coding=utf-8

from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from todo.models import TodoTarea
from todo.serializers import RegistroSerializer, TareasSerializer


class RegistroView(APIView):
    """ View para registro de usuarios"""

    def post(self, request):
        """
        Registra un nuevo usuario, retorna Ok si es que usuario fue creado
        con exito.
        ---
        request_serializer: todo.serializers.RegistroSerializer
        response_serializer: todo.serializers.RegistroSerializer
        consumes:
            - application/json
        omit_parameters:
            - form
        parameters:
            - name: Registro
              paramType: body
              pytype: todo.serializers.RegistroSerializer
              required: true
        responseMessages:
            - code: 201
              message: Created, usuario ha sido creado y registrado en BD
            - code: 400
              message: Bad Request, datos duplicados o no validos
        """
        serializer = RegistroSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        user_data = serializer.data
        user = User.objects.create_user(username=user_data["username"])
        user.set_password(user_data["password"])
        user.save()
        return Response(data=serializer.validated_data,
                        status=status.HTTP_201_CREATED)


class TareasView(APIView):
    """ View para manipulacion de tareas """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        Obtiene las tareas registradas a un determinado usuario del sistema.

        Nota para swagger:
        el argumento de 'Authorization' debe ser entregado de la siguiente forma:

         'Token 14e47cf31935b1de9c007008ef38680de16f24e3'

        anteponiendo 'Token ' al string token
        ---

        response_serializer: todo.serializers.TareasSerializer
        consumes:
            - application/json
        omit_parameters:
            -form
        parameters:
            - name: Authorization
              paramType: header
              required: true
        """
        tareas = TodoTarea.objects.filter(asignado=request.user.id)
        serializer = TareasSerializer(data=tareas, many=True)
        if serializer.is_valid():
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            # No hay tareas asignadas a este usuario
            return Response(data={}, status=status.HTTP_200_OK)
