import time
from selenium import webdriver
from selenium.webdriver.common.by import By



from rest_framework.response import Response
from rest_framework.views import APIView
from cart.models import Cart
from cart.views import calcCart
from .models import *

class CreateOrder(APIView):
    def post(self,request):
        data = request.data
        session_id = data['session_id']
        cart = Cart.objects.get(sessionID=session_id)
        order = Order.objects.create(**data)
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
