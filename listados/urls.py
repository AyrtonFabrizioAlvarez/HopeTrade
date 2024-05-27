from django.urls import path
from . import views
from intercambios import views as intercambios_views

urlpatterns = [
    path('agregar_categoria/', views.agregar_categoria, name='agregar_categoria'),
    path('listar_categorias/', views.listar_categorias, name='listar_categorias'),
    path('editar_categoria/<int:categoria_id>/', views.editar_categoria, name='editar_categoria'),
    path('eliminar_categoria/<int:categoria_id>/', views.eliminar_categoria, name='eliminar_categoria'),
    path('listar_intercambios_del_dia/', views.list_exchanges_today, name='listar_intercambios_del_dia'),
    path('listar_intercambios_del_dia/confirmar/<int:intercambio_id>/', intercambios_views.confirm_exchange, name='listar_intercambios_del_dia_confirmar'),
]