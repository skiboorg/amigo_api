from django.urls import path,include
from . import views
from .router import router
urlpatterns = [
    path('', include(router.urls)),
    path('categories', views.GetCategory.as_view()),
    path('statuses', views.GetStatus.as_view()),
    path('fill', views.Fill.as_view()),
    path('fill_contactor', views.FillContactor.as_view()),

]
