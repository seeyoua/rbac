#!/usr/bin/python3.6
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from .models import UserInfo
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler


class UserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=False, help_text="请输入邮箱")
    password = serializers.CharField(required=True, write_only=True)
    username = serializers.CharField(required=True, help_text="请输入用户名", label="用户名")
    token = serializers.CharField(read_only=True)

    def validate(self, attrs):
        username= attrs["username"]
        user = UserInfo.objects.filter(username=username).first()
        if user:
            if user.password == attrs["password"]:
                payload = jwt_payload_handler(user)
                attrs['token'] = jwt_encode_handler(payload)
                return attrs
        raise ValidationError('用户名或密码错误')

    class Meta:
        model = UserInfo
        fields = ("username", "password", "email", "token")
