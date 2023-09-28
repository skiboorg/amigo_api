from django.urls import path,include
from . import views
from .router import router
urlpatterns = [
    path('', include(router.urls)),
    path('get_clients', views.getClient),

]
