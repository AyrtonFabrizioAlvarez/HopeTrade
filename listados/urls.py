from django.urls import path
from . import views

urlpatterns = [
    path('listar_intercambios_del_dia/', views.list_exchanges_today, name='listar_intercambios_del_dia'),
]