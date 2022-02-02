# page 18
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('base_generic', views.base_generic, name='base_generic_inventoryApp'),
]
