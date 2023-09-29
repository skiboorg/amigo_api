from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models.functions import ExtractYear
from .serializers import *
from rest_framework import generics
from rest_framework import generics, viewsets, parsers
import django_filters
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
import django_filters
from rest_framework import filters
import shutil
from django.conf import settings

class ProductPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10000

    # def get_paginated_response(self, data):
    #     print(self.to_html())
    #     return Response({
    #         'links':{
    #             'next': self.get_next_link(),
    #             'prev': self.get_previous_link(),
    #         },
    #         'page_count':self.page.paginator.num_pages,
    #         'results':data
    #     })

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = ProductCategorySerializer
    queryset = ProductCategory.objects.all()
    lookup_field = 'slug'

class FilterViewSet(viewsets.ModelViewSet):
    serializer_class = FilterSerializer
    queryset = Filter.objects.all()
    lookup_field = 'slug'


class GetProductPrices(generics.ListAPIView):
    serializer_class = ProductPriceForTableSerializer
    queryset = ProductPrice.objects.all()
    pagination_class = ProductPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['weight', 'cost', 'at_store','isActive']


class GetProductsByFilter(generics.ListAPIView):
    serializer_class = ProductShortSerializer
    def get_queryset(self):
        return Product.objects.filter(category__slug=self.kwargs['cat_slug'],filters__slug__in=[self.kwargs['filter_slug']])


class ProductFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='my_custom_filter', label="Search")
    def my_custom_filter(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) |
            Q(vendorCode__icontains=value)
        )
    class Meta:
        model = Product
        fields = ['id']

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all().order_by('id')
    pagination_class = ProductPagination
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]

    filterset_class = ProductFilter


