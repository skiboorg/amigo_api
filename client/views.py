import time

from rest_framework.pagination import PageNumberPagination
from selenium import webdriver
from selenium.webdriver.common.by import By

from .serializers import *
from .models import *
from rest_framework import generics, viewsets, parsers
from rest_framework.response import Response

import django_filters
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from data.models import City
from user.models import User

class ClientPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10000


class ClientFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='my_custom_filter', label="Search")
    def my_custom_filter(self, queryset, name, value):
        return queryset.filter(
            Q(fio__icontains=value) #|
        )
    class Meta:
        model = Client
        fields = ['fio']

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    #serializer_class = ClientSerializer
    pagination_class = ClientPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ClientFilter

    def get_serializer_class(self):
        is_full = self.request.query_params.get('full',None)
        if is_full:
            return ClientSerializer
        else:
            return ClientForTableSerializer

    def create(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data['client'])
        if serializer.is_valid():
            obj = serializer.save()
            for c in request.data['contacts']:
                print(c)
                c_serializer = ContactSerializer(data=c)
                if c_serializer.is_valid():
                    c_obj = c_serializer.save()
                    c_obj.client = obj
                    c_obj.save()
                else:
                    print(serializer.errors)

        else:
            print(serializer.errors)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)




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
def getClient(request):
    user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2'
    admin_url = 'https://admin.amigovetpet.ru/'
    client_url = 'https://admin.amigovetpet.ru/client/view?id='
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

    for user_id in range(9000, 18000):
        try:
            print(f'--------------- Start user id {user_id} ------------------------')
            page_id = 1
            user_notes = []
            user_contacts = []
            user_payments = []
            user_delivery = []
            driver.get(f'https://admin.amigovetpet.ru/client/view?id={user_id}&page={page_id}')
            time.sleep(2)
            user_fio = driver.find_element(By.TAG_NAME,'h1').text
            user_attrs = driver.find_elements(By.CLASS_NAME, 'kv-attribute')
            # print(f'-------user_attrs----------')

            created_at = user_attrs[0].text
            city = user_attrs[1].text.split('/')[0].replace(' ','')
            manager = user_attrs[2].text
            address = user_attrs[3].text
            web = user_attrs[4].text
            comment = user_attrs[5].text
            status = user_attrs[6].text
            category = user_attrs[7].text.split('-')

            #print(created_at)
            #print(user_fio)

            city_obj = City.objects.filter(name=city)

            manager_obj = User.objects.filter(last_name=manager)
            #print(address)
            #print(web)
            #print(comment)

            status_obj = Status.objects.filter(name=status)
            #print(category)

            if city_obj.exists():
                city = city_obj.first()
            else:
                city = None
            if manager_obj.exists():
                manager = manager_obj.first()
            else:
                manager = User.objects.get(last_name='Person')
            if status_obj.exists():
                status = status_obj.first()
            else:
                status = Status.objects.get(name='Не определен')
            # print(manager)
            # print(city)
            # print(status)
            # print(f'-------user_attrs----------')

            new_client = Client.objects.create(
                manager= manager,
            status= status,
            city= city,
            fio= user_fio,
            web= web,
            address=address,
            comment=comment,
            created_at=created_at
            )
            print(new_client)
            for cat in category:
                cat_obj = Category.objects.get(name=cat)
                new_client.category.add(cat_obj)

            tables = driver.find_elements(By.CLASS_NAME, 'table-condensed')
            i = 0
            for table in tables:
                if i == 0:
                    user_contacts = get_from_table(table)
                if i == 1:
                    for ii in get_from_table(table): user_notes.append(ii)
                if i == 2:
                    user_payments = get_from_table(table)

                i = i + 1
            table = driver.find_element(By.CLASS_NAME, 'table-striped')
            user_delivery = get_from_table(table)
            for contact in user_contacts:
                if len(contact)>0:
                    Contact.objects.create(
                        client=new_client,
                        name=contact[1],
                        phone=contact[4],
                        email=contact[3],
                        invite=contact[6],
                        comment=contact[2],
                    )
            for delivery in user_delivery:
                if len(delivery) > 0:
                    if delivery[0] != 'Ничего не найдено.':
                        # print(delivery)
                        DeliveryAddress.objects.create(
                            old_city = delivery[0],
                        address= delivery[1],
                        flat= delivery[2],
                        comment= delivery[3],
                        client=new_client,
                        )

            for contr in user_payments:
                if len(contr) > 0:
                    if contr[0] != 'Ничего не найдено.':
                        # print(contr)
                        Contractor.objects.create(
                            name = contr[1],
                        inn= contr[2],
                        is_physic= True,
                        is_base= True if contr[3] == 'Да' else False,
                        client=new_client,
                        )


            go_next = True

            while go_next:

                next_btns = driver.find_elements(By.CLASS_NAME, 'next')
                next_btn = next_btns[0]
                next_btn_class = next_btn.get_attribute('class')

                if not 'disabled' in next_btn_class.split(' '):

                    page_id += 1
                    print(f'go to inner page {page_id}')
                    driver.get(f'https://admin.amigovetpet.ru/client/view?id={user_id}&page={page_id}')
                    tables = driver.find_elements(By.CLASS_NAME, 'table-condensed')
                    for i in get_from_table(tables[1]): user_notes.append(i)
                else:
                    print(f'stop inner pages')
                    go_next = False
            # print(f'----------------user_contacts-----------------------')
            # print(user_contacts)
            # print(f'----------------user_payments-----------------------')
            # print(user_payments)
            # print(f'----------------user_delivery-----------------------')
            # print(user_delivery)

            for note in user_notes:
                if len(note) > 0:
                    #print(note)
                    updated_at_text = note[1]
                    updated_at = None
                    author = None
                    is_done = True if note[4] == 'Выполнена' else False

                    author_last_name = note[5].split(' ')[1]
                    author_obj = User.objects.filter(last_name=author_last_name)
                    if updated_at_text !='(не задано)':
                        updated_splitted = updated_at_text.split('.')
                        updated_at = f'{updated_splitted[2]}-{updated_splitted[1]}-{updated_splitted[0]}'
                    if author_obj.exists():
                        author = author_obj.first()
                    else:
                        author = User.objects.get(last_name='Person')
                    Note.objects.create(
                        created_by = author,
                        is_done=is_done,
                        note_old_type=note[3],
                        text=note[2],
                        created_at=note[0],
                        updated_at = updated_at,
                        client=new_client
                    )
            with open("done_user.txt", "a") as myfile:
                myfile.write(f"Last done user {user_id} \r\n")
            print(f'---------------------------------------')
        except:
            print(f'--------------- Error user id {user_id} ------------------------')
            with open("user_error.txt", "a") as myfile:
                myfile.write(f"Error user id {user_id} \r\n")