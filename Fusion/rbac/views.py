from django.shortcuts import render
from rest_framework import mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .service.permissions import PermissionMixin
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler
from .serilaizers import UserSerializer
from .models import UserInfo


class LoginViewSet(PermissionMixin, APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data.get("username")
        user = UserInfo.objects.filter(username=username).first()
        self.init_permission(curret_user=user)
        return Response(serializer.data, status=status.HTTP_200_OK)


