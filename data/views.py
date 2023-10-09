import time
from datetime import datetime
import json

import django_filters
from django.db.models import Q
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from rest_framework import filters
from .models import *
from .serializers import *
from rest_framework import generics

class GetBlogItem(generics.RetrieveAPIView):
    serializer_class = BlogItemSerializer
    queryset = BlogItem.objects.filter()
    lookup_field = 'slug'

class GetTopBanners(generics.ListAPIView):
    serializer_class = TopBannerSerializer
    queryset = TopBanner.objects.all()
class CityFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='my_custom_filter', label="Search")
    def my_custom_filter(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) |
            Q(post_index__icontains=value) #|
        )
    class Meta:
        model = City
        fields = ['region']

class GetCity(generics.ListAPIView):
    serializer_class = CitySerializer
    queryset = City.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = CityFilter

class GetBanners(generics.ListAPIView):
    serializer_class = BannerSerializer
    queryset = Banner.objects.all()
class GetNews(generics.ListAPIView):
    serializer_class = BlogItemSerializer

    def get_queryset(self):
        item_type = self.request.query_params.get('item_type')
        index = self.request.query_params.get('index', None)

        if item_type == 'news':
            qs = BlogItem.objects.filter(is_news_item=True)
        else:
            qs = BlogItem.objects.filter(is_news_item=False)

        if index:
            qs = qs[:3]

        return qs


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

def getCities(request):
    user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2'
    admin_url = 'https://admin.amigovetpet.ru/'
    page_url = 'https://admin.amigovetpet.ru/city/view?id='
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

    for page_id in range(1,1500):
        try:
            driver.get(f'{page_url}{page_id}')
            table = driver.find_element(By.CLASS_NAME, 'table')
            result = get_from_table(table)
            City.objects.create(
                name=result[0][0],
                timezone=result[1][0],
                country=result[2][0],
                post_index=result[3][0],
                region=result[4][0],
                area=result[5][0],
                type=result[6][0],
                latitude=result[7][0],
                longtitude=result[8][0],
            )
        except:
            print(f'page id {page_id} error')
    return HttpResponse('OK')