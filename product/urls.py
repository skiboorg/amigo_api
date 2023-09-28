from django.urls import path,include
from . import views
from .router import router
urlpatterns = [
    path('', include(router.urls)),
    path('filter/<cat_slug>/<filter_slug>', views.GetProductsByFilter.as_view()),
    path('prices', views.GetProductPrices.as_view()),


]
