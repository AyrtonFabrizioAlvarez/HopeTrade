from django.urls import path
from . import views

urlpatterns = [
    path('agregar_categoria/', views.agregar_categoria, name='agregar_categoria'),
    path('listar_categorias/', views.listar_categorias, name='listar_categorias'),
    path('editar_categoria/<int:categoria_id>/', views.editar_categoria, name='editar_categoria'),
    path('eliminar_categoria/<int:categoria_id>/', views.eliminar_categoria, name='eliminar_categoria')
]