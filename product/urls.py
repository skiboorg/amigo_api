from django.urls import path,include
from . import views
from .router import router
urlpatterns = [
    path('', include(router.urls)),
    path('filter/<cat_slug>/<filter_slug>', views.GetProductsByFilter.as_view()),
    path('prices', views.GetProductPrices.as_view()),
    path('fill_cat', views.FillCat.as_view()),
    path('fill_product', views.FillProd.as_view()),
    path('fill_fasovka', views.FillFas.as_view()),


]
