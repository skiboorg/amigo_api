
from django.utils import timezone
from datetime import timedelta

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.db import IntegrityError, transaction

from rest_framework import exceptions, serializers, status, generics
from .models import *

from django.contrib.auth.tokens import default_token_generator


import logging
logger = logging.getLogger(__name__)

class ContractorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contractor
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'

class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = '__all__'

class DeliveryAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeliveryAddress
        fields = '__all__'

class NoteSerializer(serializers.ModelSerializer):
    from user.serializers import UserSerializer
    created_by = UserSerializer(many=False, read_only=True, required=False)
    class Meta:
        model = Note
        fields = '__all__'

class StatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Status
        ref_name = 'client_status'
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    from data.serializers import CitySerializer
    from user.serializers import UserSerializer

    contacts = ContactSerializer(many=True, read_only=True, required=False)
    category = CategorySerializer(many=True, read_only=True, required=False)
    city = CitySerializer(many=False, read_only=True, required=False)
    manager = UserSerializer(many=False, read_only=True, required=False)
    status = StatusSerializer(many=False, read_only=True, required=False)
    notes = NoteSerializer(many=True, read_only=True, required=False)
    contractors = ContractorSerializer(many=True, read_only=True, required=False)
    delivery_addresses = DeliveryAddressSerializer(many=True, read_only=True, required=False)
    orders = serializers.SerializerMethodField()
    class Meta:
        model = Client
        fields = '__all__'

    def get_orders(self,obj):
        from order.serializers import OrderSerializer
        if obj.orders:
            return OrderSerializer(obj.orders, many=True).data


class ClientForTableSerializer(serializers.ModelSerializer):
    from data.serializers import CitySerializer
    from user.serializers import UserSerializer
    city = CitySerializer(many=False, read_only=True, required=False)
    manager = UserSerializer(many=False, read_only=True, required=False)
    status = StatusSerializer(many=False, read_only=True, required=False)
    class Meta:
        model = Client
        fields = '__all__'


class ClientShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'





