from django.urls import path,include
from . import views
from .router import router

urlpatterns = [
    path('', include(router.urls)),
    path('create', views.CreateOrder.as_view()),
    path('get_orders', views.getOrders),
    path('update_price', views.UpdateOrderItem.as_view()),

]
