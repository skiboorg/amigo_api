
from django.utils import timezone
from datetime import timedelta

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.db import IntegrityError, transaction

from rest_framework import exceptions, serializers, status, generics

import settings
from .models import *



class BlogCategorySerializer(serializers.ModelSerializer):
        model = BlogCategory
        fields = '__all__'

class BlogItemSerializer(serializers.ModelSerializer):
    category = BlogCategorySerializer(many=False, required=False, read_only=True)
    class Meta:
        model = BlogItem
        fields = '__all__'

















