
from django.utils import timezone
from datetime import timedelta

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.db import IntegrityError, transaction

from rest_framework import exceptions, serializers, status, generics

import settings
from .models import *

class ProductGalleryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductGalleryImage
        fields = '__all__'

class ProductPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPrice
        fields = '__all__'


class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    gallery = ProductGalleryImageSerializer(many=True, required=False, read_only=True)
    productType = ProductTypeSerializer(many=True, required=False, read_only=True)
    prices = ProductPriceSerializer(many=True, required=False, read_only=True)
    class Meta:
        model = Product
        fields = '__all__'


class ProductShortSerializer(serializers.ModelSerializer):
    prices = ProductPriceSerializer(many=True, required=False, read_only=True)
    image = serializers.SerializerMethodField()
    productType = ProductTypeSerializer(many=True, required=False, read_only=True)
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'slug',
            'shortDescription',
            'image',
            'prices',
            'productType'
        ]

    def get_image(self, obj):
        if obj.gallery.all().filter(is_main=True):
            return f'{settings.SITE_URL}{obj.gallery.all().filter(is_main=True).first().image.url}'
        else:
            return f'{settings.SITE_URL}{obj.gallery.all().first().image.url}'



class ProductCartSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'slug',
            'shortDescription',
            'image',
            'prices',
        ]

    def get_image(self, obj):
        if obj.gallery.all().filter(is_main=True):
            return f'{settings.SITE_URL}{obj.gallery.all().filter(is_main=True).first().image.url}'
        else:
            return f'{settings.SITE_URL}{obj.gallery.all().first().image.url}'











