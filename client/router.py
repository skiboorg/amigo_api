from rest_framework import routers
from .views import *
router = routers.SimpleRouter(trailing_slash=False)
router.register(r'clients', ClientViewSet)
router.register(r'contacts', ContactViewSet)
router.register(r'notes', NoteViewSet)
router.register(r'contractors', ContractorViewSet)
router.register(r'addresses', AddressViewSet)


