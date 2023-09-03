from django.urls import path,include
from . import views

urlpatterns = [
    path('categories', views.GetCategories.as_view()),
    path('all', views.GetProducts.as_view()),
    path('by_subcategory/<slug>', views.GetProductsBySubcategory.as_view()),
    path('<slug>', views.GetProduct.as_view()),

]
