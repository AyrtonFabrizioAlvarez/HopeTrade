from django.urls import path
from . import views

urlpatterns = [
    path('listar_estadisticas/', views.listar_estadisticas, name='listar_estadisticas'),
    path('estadisticas_publicaciones/', views.estadisticas_publicaciones, name='estadisticas_publicaciones'),
]