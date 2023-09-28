
from django.utils import timezone
from datetime import timedelta

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.db import IntegrityError, transaction

from rest_framework import exceptions, serializers, status, generics

import settings
from .models import *


class TopBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopBanner
        fields = '__all__'
class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'

class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = '__all__'

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'

class BlogItemSerializer(serializers.ModelSerializer):
    category = BlogCategorySerializer(many=False, required=False, read_only=True)
    class Meta:
        model = BlogItem
        fields = '__all__'

















