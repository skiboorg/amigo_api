
from django.utils import timezone
from datetime import timedelta

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.db import IntegrityError, transaction

from rest_framework import exceptions, serializers, status, generics

import settings
from order.models import OrderItem





class OrderItemSerializer(serializers.ModelSerializer):
    from product.serializers import ProductCartSerializer,ProductPriceSerializer

    product = ProductCartSerializer(many=False, required=False, read_only=True)
    productPrice = ProductPriceSerializer(many=False, required=False, read_only=True)
    order_date = serializers.SerializerMethodField()

    class Meta:
        ref_name='rep_item'
        model = OrderItem
        fields = '__all__'

    def get_order_date(self,obj):
        return obj.order.created_at_date



















