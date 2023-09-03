
from django.utils import timezone
from datetime import timedelta

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.db import IntegrityError, transaction

from rest_framework import exceptions, serializers, status, generics

import settings
from .models import *



class CartItemSerializer(serializers.ModelSerializer):
    from product.serializers import ProductCartSerializer,ProductPriceSerializer
    product = ProductCartSerializer(many=False, required=False, read_only=True)
    productPrice = ProductPriceSerializer(many=False, required=False, read_only=True)
    class Meta:
        model = CartItem
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    products = CartItemSerializer(many=True, required=False, read_only=True)
    class Meta:
        model = Cart
        fields = '__all__'

















