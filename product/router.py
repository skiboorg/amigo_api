from rest_framework import routers
from .views import *

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'items', ProductViewSet)
router.register(r'category', CategoryViewSet)
router.register(r'filter', FilterViewSet)


