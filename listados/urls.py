from django.urls import path
from . import views
from intercambios import views as intercambios_views

urlpatterns = [
    path('listar_intercambios_del_dia/', views.list_exchanges_today, name='listar_intercambios_del_dia'),
    path('listar_intercambios_del_dia/confirmar/<int:intercambio_id>/', intercambios_views.confirm_exchange, name='listar_intercambios_del_dia_confirmar'),
]