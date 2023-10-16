from rest_framework import routers
from .views import *

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'orders', OrderViewSet)
router.register(r'order_items', OrderItemViewSet)
router.register(r'delivery', DeliveryViewSet)
router.register(r'delivery_company', DeliveryCompanyViewSet)
router.register(r'delivery_status', DeliveryStatusViewSet)
router.register(r'payment_type', PaymentTypeViewSet)
router.register(r'status', StatusViewSet)



