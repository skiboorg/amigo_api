from django.urls import path,include
from . import views
from .router import router
urlpatterns = [
    path('get_clients', views.getClient),

]
