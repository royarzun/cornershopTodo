# coding=utf-8

from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from todo.serializers import RegistroSerializer


class RegistroView(APIView):
    """

    """
    def post(self, request):
        serializer = RegistroSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        user_data = serializer.data
        user = User.objects.create_user(username=user_data["username"])
        user.set_password(user_data["password"])
        user.save()
        return Response(data="user created", status=status.HTTP_201_CREATED)
