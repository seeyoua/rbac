#!/usr/bin/python3.6
#--*-- coding:utf-8 --*--
#@Time  : 2020/3/25 22:55
#@Auhor : rain
#@Site  : 
#@File  : serializers.py
#@Software : untitled
import re
from rest_framework import serializers
from .models import Customer, Payment
from django.conf import settings


class CustomersSerializers(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True)
    name = serializers.CharField(max_length=32, required=True, help_text="客户名称", label="客户")
    age = serializers.CharField(max_length=32, required=True, help_text="年龄", label="年龄")
    email = serializers.CharField(max_length=32, required=True, help_text="邮箱", label="邮箱")

    def validate_email(self, email):
        # 验证邮箱号码是否合法
        if not re.match(settings.REGEX_EMAIL, email):
            raise serializers.ValidationError('邮箱号码非法')
        return email

    class Meta:
        model = Customer
        fields = ("uuid", "name", "age", "email")


class PaymentSerializer(serializers.ModelSerializer):

    customer = CustomersSerializers()
    uuid = serializers.UUIDField(read_only=True)

    class Meta:
        model = Payment
        fields = ("uuid", "title", "money", "customer")
