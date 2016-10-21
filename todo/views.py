# coding=utf-8

from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from todo.serializers import RegistroSerializer


class RegistroView(APIView):
    """ View para registro de usuarios"""

    def post(self, request):
        """
        Registra un nuevo usuario, retorna Ok si es que usuario fue creado
        con exito.
        ---
        parameters_strategy:
            form: replace
        parameters:
            - name: username
              type: string
              description: Nombre de usuario a crear
              required: True
            - name: password
              type: string
              description: Password correspondiente a este usuario
              required: True
        responseMessages:
            - code: 201
              message: Created, usuario ha sido creado y registrado en BD
            - code: 400
              message: Bad Request, faltan datos o datos son no validos
        """
        serializer = RegistroSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        user_data = serializer.data
        user = User.objects.create_user(username=user_data["username"])
        user.set_password(user_data["password"])
        user.save()
        return Response(data="Ok", status=status.HTTP_201_CREATED)
