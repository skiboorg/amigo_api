from django.urls import path,include
from . import views

urlpatterns = [

    path('get_cities', views.getCities),
    path('news', views.GetNews.as_view()),
    path('cities', views.GetCity.as_view()),
    path('top_banners', views.GetTopBanners.as_view()),
    path('banners', views.GetBanners.as_view()),
    path('blog/<slug>', views.GetBlogItem.as_view()),

]
