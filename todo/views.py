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
