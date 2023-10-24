
from django.utils import timezone
from datetime import timedelta

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.db import IntegrityError, transaction

from rest_framework import exceptions, serializers, status, generics

import settings
from .models import *


class FeedbackImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackImage
        fields = '__all__'


class FeedbackSerializer(serializers.ModelSerializer):
    images = FeedbackImageSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Feedback
        fields = '__all__'
class ProductGalleryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductGalleryImage
        fields = '__all__'


class ProductPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPrice
        fields = '__all__'

class ProductTabSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTab
        fields = '__all__'


class FilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filter
        fields = '__all__'


class ProductCategorySerializer(serializers.ModelSerializer):
    filters = FilterSerializer(many=True, required=False, read_only=True)
    class Meta:
        model = ProductCategory
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    gallery = ProductGalleryImageSerializer(many=True, required=False, read_only=True)
    filters = FilterSerializer(many=True, required=False, read_only=True)
    prices = ProductPriceSerializer(many=True, required=False, read_only=True)
    tabs = ProductTabSerializer(many=True, required=False, read_only=True)
    feedbacks = FeedbackSerializer(many=True, required=False, read_only=True)
    category = ProductCategorySerializer(many=False, required=False, read_only=True)
    class Meta:
        model = Product
        fields = '__all__'


class ProductShortSerializer(serializers.ModelSerializer):
    prices = ProductPriceSerializer(many=True, required=False, read_only=True)
    image = serializers.SerializerMethodField()
    filters = FilterSerializer(many=True, required=False, read_only=True)
    class Meta:
        model = Product
        fields = [
            'id',
            'vendorCode',
            'name',
            'slug',
            'shortDescription',
            'image',
            'prices',
            'filters',
            'isNew',
            'isDiscount',
            'discount',
        ]

    def get_image(self, obj):
        if obj.gallery.all().filter(is_main=True):
            return f'{settings.SITE_URL}{obj.gallery.all().filter(is_main=True).first().image.url}'
        else:
            return f'{settings.SITE_URL}{obj.gallery.all().first().image.url}'


class ProductCartSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    #prices = ProductPriceSerializer(many=True, required=False, read_only=True)
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
        if len(obj.gallery.all())>0:
            if obj.gallery.all().filter(is_main=True):
                return f'{settings.SITE_URL}{obj.gallery.all().filter(is_main=True).first().image.url}'
            else:
                return f'{settings.SITE_URL}{obj.gallery.all().first().image.url}'


class ProductForTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductPriceForTableSerializer(serializers.ModelSerializer):
    product = ProductForTableSerializer(many=False, required=False, read_only=True)

    class Meta:
        model = ProductPrice
        fields = '__all__'


