
from django.utils import timezone
from datetime import timedelta

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.db import IntegrityError, transaction

from rest_framework import exceptions, serializers, status, generics

import settings
from .models import *



class OrderItemSerializer(serializers.ModelSerializer):
    from product.serializers import ProductCartSerializer,ProductPriceSerializer
    product = ProductCartSerializer(many=False, required=False, read_only=True)
    productPrice = ProductPriceSerializer(many=False, required=False, read_only=True)
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    products = OrderItemSerializer(many=True, required=False, read_only=True)
    class Meta:
        model = Order
        fields = '__all__'

















