from rest_framework import routers
from .views import *

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'items', ProductViewSet)
router.register(r'price', ProductPriceViewSet)
router.register(r'tabs', ProductTabViewSet)
router.register(r'images', ProductImagesViewSet)
router.register(r'category', CategoryViewSet)
router.register(r'filter', FilterViewSet)


