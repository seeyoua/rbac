from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from rest_framework import mixins
from .models import Payment, Customer
from .serializers import CustomersSerializers, PaymentSerializer


class CustomerViewSet(mixins.ListModelMixin, mixins.DestroyModelMixin,
                      mixins.CreateModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomersSerializers


class PaymentViewSet(mixins.ListModelMixin, mixins.DestroyModelMixin,
                    mixins.CreateModelMixin, mixins.RetrieveModelMixin, GenericViewSet):

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class CustomerImportCsv(APIView):

    def post(self, request):
        request.files.Get()
