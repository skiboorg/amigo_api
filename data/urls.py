from django.urls import path,include
from . import views

urlpatterns = [

    path('get_cities', views.getCities),
    path('news', views.GetNews.as_view()),
    path('blog/<slug>', views.GetBlogItem.as_view()),

]
