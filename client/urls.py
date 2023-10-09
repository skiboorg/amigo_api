from django.urls import path,include
from . import views
from .router import router
urlpatterns = [
    path('', include(router.urls)),
    path('categories', views.GetCategory.as_view()),
    path('statuses', views.GetStatus.as_view()),
    path('get_clients', views.getClient),

]
