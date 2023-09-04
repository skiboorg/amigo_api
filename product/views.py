from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models.functions import ExtractYear
from .serializers import *
from rest_framework import generics
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.shortcuts import get_object_or_404
import django_filters

import shutil
from django.conf import settings



class GetCategories(generics.ListAPIView):
    serializer_class = ProductCategorySerializer
    queryset = ProductCategory.objects.all()

class GetProducts(generics.ListAPIView):
    serializer_class = ProductShortSerializer
    queryset = Product.objects.filter(isActive=True)

class GetProductsBySubcategory(generics.ListAPIView):
    serializer_class = ProductShortSerializer
    def get_queryset(self):
        return Product.objects.filter(subCategory__slug=self.kwargs['slug'])

class GetCatalog(generics.ListAPIView):
    serializer_class = ProductShortSerializer
    def get_queryset(self):
        return Product.objects.filter(category__slug=self.kwargs['cat_slug'],subCategory__slug=self.kwargs['subcat_slug'])

class GetProduct(generics.RetrieveAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_field = 'slug'
