from django.urls import path,include
from . import views

urlpatterns = [
    path('products', views.OrderProducts.as_view()),
    path('managers', views.ManagersReport.as_view()),
    path('categories', views.CategoriesReport.as_view()),
    path('common', views.CommonReport.as_view()),


]
