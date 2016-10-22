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
            - form
        parameters:
            - name: Authorization
              paramType: header
              required: true
        responseMessages:
            - code: 200
              message: Ok, retorna tareas de usuario
            - code: 401
              message: UNAUTHORIZED, malas credenciales
        """
        tareas = TodoTarea.objects.filter(asignado=request.user)
        serializer = TareasSerializer(tareas, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Crea una tarea TODO para este usuario.

        Nota para swagger:
        el argumento de 'Authorization' debe ser entregado de la siguiente forma:

         'Token 14e47cf31935b1de9c007008ef38680de16f24e3'

        anteponiendo 'Token ' al string token
        ---
        request_serializer: todo.serializers.TareasSerializer
        consumes:
            - application/json
        omit_parameters:
            - form
        parameters:
            - name: Authorization
              paramType: header
              required: true
            - name: Tarea
              paramType: body
              pytype: todo.serializers.TareasSerializer
              required: true
        responseMessages:
            - code: 201
              message: Created, tarea fue creada
            - code: 400
              message: Bad request, tarea no valida
            - code: 401
              message: UNAUTHORIZED, malas credenciales
        """
        serializer = TareasSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            tarea_data = serializer.data
            tarea = TodoTarea(asignado=request.user, **tarea_data)
            tarea.save()
            return Response(tarea.id, status=status.HTTP_201_CREATED)


class TareaView(APIView):

    def get(self, request, tarea_id):
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
            - form
        parameters:
            - name: Authorization
              paramType: header
              required: true
            - name: tarea_id
              description: id de la tarea
              required: True
              paramType: path
              type: int
        responseMessages:
            - code: 200
              message: Ok, retorna tareas de usuario
            - code: 400
              message: Bad request, tarea no existe
            - code: 401
              message: UNAUTHORIZED, malas credenciales
        """
        try:
            tarea = TodoTarea.objects.get(id=tarea_id)
            serializer = TareasSerializer(tarea)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except TodoTarea.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, tarea_id):
        """ Modifica/Update una tarea existente

        Nota para swagger:
        el argumento de 'Authorization' debe ser entregado de la siguiente forma:

         'Token 14e47cf31935b1de9c007008ef38680de16f24e3'

        anteponiendo 'Token ' al string token
        ---
        request_serializer: todo.serializers.TareasSerializer
        consumes:
            - application/json
        omit_parameters:
            - form
        parameters:
            - name: tarea_id
              description: id de la tarea
              required: True
              paramType: path
              type: int
            - name: Authorization
              paramType: header
              required: true
            - name: Tarea
              paramType: body
              pytype: todo.serializers.TareasSerializer
              required: true
        responseMessages:
            - code: 200
              message: Ok, tarea fue modificada
            - code: 400
              message: Bad request, tarea a modificar no existe
            - code: 401
              message: UNAUTHORIZED, malas credenciales
        """
        serializer = TareasSerializer(data=request.data)
        if serializer.is_valid():
            try:
                tarea = TodoTarea.objects.get(id=tarea_id)
                for attr, value in serializer.data.items():
                    setattr(tarea, attr, value)
                tarea.save()
                reserializer = TareasSerializer(tarea, many=False)
                return Response(reserializer.data, status=status.HTTP_200_OK)
            except TodoTarea.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
           return Response(status=status.HTTP_400_BAD_REQUEST)