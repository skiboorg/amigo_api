import time
from _decimal import Decimal

from rest_framework.pagination import PageNumberPagination
from rest_framework import generics, viewsets, parsers

from django_filters import IsoDateTimeFilter
import django_filters
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.views import APIView

from .serializers import *
from rest_framework.response import Response

from order.models import Order,OrderItem
from user.models import User
from product.models import ProductCategory
from client.models import Client

from datetime import datetime
import dateutil.relativedelta

from django.db.models import Sum

class OrderProductPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10000

    # def get_paginated_response(self, data):
    #     total_items = self.page.paginator.count  # Общее количество товаров
    #
    #
    #     return Response({
    #         'count': total_items,
    #         'page_size': self.page_size,
    #         'page_number': self.page.number,
    #         'results': data
    #     })


class OrderProductFilter(django_filters.FilterSet):
    created_at_gte = IsoDateTimeFilter(field_name="order__created_at_date", lookup_expr='gte')
    created_at_lte = IsoDateTimeFilter(field_name="order__created_at_date", lookup_expr='lte')
    # q = django_filters.CharFilter(method='my_custom_filter', label="Search")
    # def my_custom_filter(self, queryset, name, value):
    #     return queryset.filter(
    #         Q(product_id__exact=value) #|
    #     )
    class Meta:
        model = OrderItem
        fields = ['product_id']

class OrderProducts(generics.ListAPIView):
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()
    pagination_class = OrderProductPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = OrderProductFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        serializer = self.get_serializer(page, many=True)
        # serializer = self.get_serializer(queryset, many=True)
        total_items = 0
        total_price = Decimal(0)
        for item in queryset:
            print(item.total_price)
            total_price += item.total_price
            total_items += item.amount

        # Создайте пользовательский словарь с данными, которые вы хотите включить в ответ
        custom_data = {
            'total_items': total_items,
            'total_price': total_price,
            'custom_field_2': 'Значение 2',
        }

        # Включите данные из сериализатора и пользовательские данные в ответ
        response_data = {
            'results': serializer.data,
            'custom_data': custom_data,
            'count': queryset.count(),
        }

        return Response(response_data)


class CommonReport(APIView):
    def get(self, request):
        result = {}
        orders = Order.objects.all()
        clients = Client.objects.all()
        result['orders'] = orders.count()
        result['clients'] = clients.count()

        return Response(result, status=200)
class CategoriesReport(APIView):
    def get(self, request):
        categories = ProductCategory.objects.all()
        result = []
        for category in categories:
            order_items = OrderItem.objects.filter(product__category=category)
            order_items_filtered = order_items.filter(
                order__created_at_date__range=[self.request.query_params.get('date_start'),
                                               self.request.query_params.get('date_end')])
            print('order_items_filtered',order_items_filtered)
            for i in order_items_filtered:
                print(i.amount)
            print('order_items',order_items)
            result.append({
                "name":category.name,
                "orders_count":order_items_filtered.count(),
                "products_count":order_items_filtered.aggregate(Sum('amount'))['amount__sum'],
                "total_price": order_items_filtered.aggregate(Sum('total_price'))['total_price__sum']
            })
        return Response(result,status=200)
class ManagersReport(APIView):
    def get(self,request):
        year = self.request.query_params.get('year')
        month = self.request.query_params.get('month')
        prev_period = datetime.strptime(f'01/{month}/{year}', '%d/%m/%Y')+ dateutil.relativedelta.relativedelta(months=-1)
        print(prev_period.year)
        managers = User.objects.filter(is_manager=True)
        result = []
        for manager in managers:
            total_orders = Order.objects.filter(manager=manager)
            orders_in_current_period = Order.objects.filter(manager=manager,created_at_date__year=year,created_at_date__month=month)
            orders_in_prev_period = Order.objects.filter(manager=manager,created_at_date__year=prev_period.year,created_at_date__month=prev_period.month)
            print(manager)
            print(orders_in_current_period.count())
            print(orders_in_prev_period.count())
            print(total_orders.count())
            result.append({
                "fio":manager.fio,
                "total_clients":total_orders.count(),
                "orders_in_current_period":orders_in_current_period.count(),
                "orders_in_prev_period":orders_in_prev_period.count(),
                "total_price": orders_in_current_period.aggregate(Sum('total_price'))['total_price__sum']

            })
        return Response(result,status=200)