import time

from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from selenium import webdriver
from selenium.webdriver.common.by import By



from rest_framework.response import Response
from rest_framework.views import APIView
from cart.models import Cart
from cart.views import calcCart
from .models import *
from user.models import User
from client.models import Client
from product.services import create_random_string
from .serializers import *
from django_filters import IsoDateTimeFilter
import django_filters
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


def calcOrder(order_id):
    order = Order.objects.get(id=order_id)
    total_price = Decimal(0)
    total_weight = Decimal(0)
    for product in order.products.all():
        print(product)
        product.total_price = 0
        product.total_price+= product.price_with_discount * product.amount
        total_price+= product.total_price
        product.total_weight = 0
        product.total_weight += product.productPrice.weight * product.amount
        total_weight += product.total_weight
        product.save()
    order.total_price = total_price
    order.total_weight = total_weight
    order.save()

class OrderItemViewSet(viewsets.ModelViewSet):

    serializer_class = OrderItem
    queryset = OrderItem.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        order_id = instance.order.id
        self.perform_destroy(instance)
        calcOrder(order_id)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        print(obj)
        print(request.data)
        obj.amount = request.data['amount']
        obj.price_with_discount = request.data['price_with_discount']
        obj.save()
        calcOrder(request.data['order'])
        return Response(status=200)

class OrderPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10000



class OrderFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='my_custom_filter', label="Search")
    created_at_gte = IsoDateTimeFilter(field_name="created_at_date", lookup_expr='gte')
    created_at_lte = IsoDateTimeFilter(field_name="created_at_date", lookup_expr='lte')
    total_price_gte = django_filters.NumberFilter(field_name="total_price", lookup_expr='gte')
    total_price_lte = django_filters.NumberFilter(field_name="total_price", lookup_expr='lte')
    def my_custom_filter(self, queryset, name, value):
        return queryset.filter(
            Q(client__fio__icontains=value)

        )
    class Meta:
        model = Order
        fields = ['status__id','manager__id','payment_type__id']

class OrderViewSet(viewsets.ModelViewSet):
    pagination_class = OrderPagination
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    filterset_class = OrderFilter

    def get_serializer_class(self):
        is_edit = self.request.query_params.get('edit',None)
        if is_edit:
            return OrderEditSerializer
        else:
            return OrderSerializer

    # def perform_create(self, serializer):
    #     print(serializer)

    def create(self, request, *args, **kwargs):
        data = request.data
        #print(data)
        new_order = Order.objects.create(
            client_id=data.get('client',None),
            contact_id=data.get('contact',None),
            contractor_id=data.get('contractor',None),
        )

        for product in data['products']:
            print(product)
            OrderItem.objects.create(
                order=new_order,
                product_id=product['productPrice']['product'],
                productPrice_id=product['productPrice']['id'],
                price_with_discount=product['price_with_discount'],
                amount=product['amount']
            )
        return Response(status=200)

    def update(self, request, *args, **kwargs):
        data = request.data
        print(data)
        instance = self.get_object()
        client_id = data.get('client',None)
        status_id = data.get('status',None)
        contact_id = data.get('contact',None)
        contractor_id = data.get('contractor',None)
        manager_id = data.get('manager',None)
        if client_id:
            instance.client_id = client_id
        if contact_id:
            instance.contact_id = contact_id
        if contractor_id:
            instance.contractor_id = contractor_id
        if manager_id:
            instance.manager_id = manager_id
        if status_id:
            instance.status_id = status_id
        instance.save()
        products = data.get('products', None)
        if products:
            for product in products:
                print(product)
                OrderItem.objects.create(
                    order=instance,
                    product_id=product['productPrice']['product'],
                    productPrice_id=product['productPrice']['id'],
                    price_with_discount=product['price_with_discount'],
                    amount=product['amount']
                )
            calcOrder(instance.id)
        return Response(status=200)

class UpdateOrderItem(APIView):
    def post(self, request):
        data = request.data
        print(data)
        return Response(status=200)

class CreateOrder(APIView):

    def post(self,request):
        data = request.data
        session_id = data['session_id']
        new_user = data.get('new_user', None)
        user = None
        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user)
        else:
            cart = Cart.objects.get(sessionID=session_id)

        if new_user:
            email = data['email']
            fio = data['fio']
            client = Client.objects.create(
                fio=fio
            )
            password = create_random_string(digits=False, num=8)
            print(password)
            user = User.objects.create_user(
                client=client,
                login=email,
                email=email,
                password=password
            )

        if new_user:
            order = Order.objects.create(
                user=user,
            )
        else:
            order = Order.objects.create(
                session_id=session_id,
            )
        order.totalPrice = cart.totalPrice
        order.save()
        for cart_product in cart.products.all():
            OrderItem.objects.create(
                order=order,
                product=cart_product.product,
                productPrice=cart_product.productPrice,
                amount=cart_product.amount,
                totalPrice=cart_product.totalPrice,

            )
            cart_product.delete()
            calcCart(cart)

        return Response(status=200)

class DeliveryViewSet(viewsets.ModelViewSet):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
class DeliveryCompanyViewSet(viewsets.ModelViewSet):
    queryset = DeliveryCompany.objects.all()
    serializer_class = DeliveryCompanySerializer

class PaymentTypeViewSet(viewsets.ModelViewSet):
    queryset = PaymentType.objects.all()
    serializer_class = PaymentTypeSerializer

class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
def get_from_table(table):
    rows = table.find_elements(By.TAG_NAME,'tr')

    # Создать список для хранения данных
    data_list = []

    # Проход по каждой строке и извлечение данных из ячеек (td)
    for row in rows:
        # Получить все ячейки (td) из текущей строки
        cells = row.find_elements(By.TAG_NAME,'td')
        row_data = []

        # Проход по каждой ячейке и добавление ее содержимого в список данных текущей строки
        for cell in cells:
            row_data.append(cell.text)

        # Добавление списка данных текущей строки в общий список данных
        data_list.append(row_data)

    # Вывод результатов
    # for row_data in data_list:
    #     print(row_data)
    return data_list
def getOrders(request):
    user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2'
    admin_url = 'https://admin.amigovetpet.ru/'
    client_url = 'https://admin.amigovetpet.ru/order/view?id='
    login = 'shumilova'
    password = '7Bm9otUT'
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument(f'user-agent={user_agent}')
    driver = webdriver.Chrome('/home/xxx/chromedriver', chrome_options=chrome_options)

    driver.get(admin_url)

    content = driver.page_source
    login_input = driver.find_element(By.ID, 'loginform-username')
    password_input = driver.find_element(By.ID, 'loginform-password')
    login_button = driver.find_element(By.CLASS_NAME, 'btn-info')

    login_input.send_keys(login)
    password_input.send_keys(password)
    login_button.click()
    time.sleep(2)

    for page_id in range(30000, 35000):
        try:
            driver.get(f'https://admin.amigovetpet.ru/order/view?id={page_id}')
            time.sleep(2)
            user_attrs = driver.find_elements(By.CLASS_NAME, 'kv-attribute')
            fields = ['Клиент', 'Контрагент', 'Менеджер','Адрес', 'Почта','Имя', 'Телефон','Дата заказа', 'Сумма', 'Сум.доставки', 'Оплата','Метод доставки','Комментарий','Время заказа', 'Включить доставку в товар?','Промо-код', 'Статус', 'Статус обмена', 'Архив']
            order_info = """"""
            order_items_text = """"""
            order_payments_text = """"""
            atr_index = 0
            for attr in user_attrs:
                print(attr.text)
                order_info += f'{fields[atr_index]} : {attr.text} \r\n'
                atr_index += 1

            tables = driver.find_elements(By.CLASS_NAME, 'table-condensed')
            order_items = []
            order_payments = []
            i = 0
            for table in tables:
                if i == 0:
                    order_items = get_from_table(table)
                if i == 1:
                    order_payments = get_from_table(table)
                i+=1

            for j in order_items:
                if len(j)>0:
                    order_items_text += ('|').join(j) + '\r\n'
            for j in order_payments:
                if len(j)>0:
                    order_payments_text += ('|').join(j) + '\r\n'
            print(order_items_text)
            print(order_payments_text)


            Order.objects.create(order_old_data=order_info, order_old_id=page_id, order_old_items=order_items_text,order_old_payments = order_payments_text)
        except:
            pass
