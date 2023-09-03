from django.urls import path,include
from . import views

urlpatterns = [
    path('update', views.UpdateCart.as_view()),
    path('<session_id>', views.GetCart.as_view()),

]
