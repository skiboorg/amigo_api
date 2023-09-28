
from django.utils import timezone
from datetime import timedelta

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.db import IntegrityError, transaction

from rest_framework import exceptions, serializers, status, generics

import settings
from .models import *

class DeliverySerializer(serializers.ModelSerializer):

    class Meta:
        model = Delivery
        fields = '__all__'

class DeliveryCompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = DeliveryCompany
        fields = '__all__'

class PaymentTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentType
        fields = '__all__'

class StatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Status
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    from product.serializers import ProductCartSerializer,ProductPriceSerializer

    product = ProductCartSerializer(many=False, required=False, read_only=True)
    productPrice = ProductPriceSerializer(many=False, required=False, read_only=True)

    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    from data.serializers import CitySerializer
    from user.serializers import UserSerializer
    from client.serializers import ClientShortSerializer, ContractorSerializer, ContactSerializer
    products = OrderItemSerializer(many=True, required=False, read_only=True)
    city = CitySerializer(many=False, required=False, read_only=True)
    client = ClientShortSerializer(many=False, required=False, read_only=True)
    contractor = ContractorSerializer(many=False, required=False, read_only=True)
    manager = UserSerializer(many=False, required=False, read_only=True)
    contact = ContactSerializer(many=False, required=False, read_only=True)
    delivery = DeliverySerializer(many=False, required=False, read_only=True)
    delivery_company = DeliveryCompanySerializer(many=False, required=False, read_only=True)
    payment_type = PaymentTypeSerializer(many=False, required=False, read_only=True)
    status = StatusSerializer(many=False, required=False, read_only=True)
    class Meta:
        model = Order
        fields = '__all__'

















