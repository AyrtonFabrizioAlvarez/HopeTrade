from django.urls import path
from . import views

urlpatterns = [
    path('publicaciones_sistema/', views.historial_publicaciones_sistema, name='historial_publicaciones_sistema'),
    path('intercambios_sistema/', views.historial_intercambios_sistema, name='historial_intercambios_sistema'),
    path('donaciones_sistema/', views.historial_donaciones_sistema, name='historial_donaciones_sistema'),
    path('donaciones_dinero_sistema/', views.historial_donaciones_dinero_sistema, name='historial_donaciones_dinero_sistema'),
    path('donaciones_productos_sistema/', views.historial_donaciones_productos_sistema, name='historial_donaciones_productos_sistema'),
    path('publicaciones_usuario/<int:user_id>/', views.historial_publicaciones_usuario, name='historial_publicaciones_usuario'),
    path('intercambios_usuario/<int:user_id>/', views.historial_intercambios_usuario, name='historial_intercambios_usuario'),
    path('filtrar_historial_publicaciones/', views.filtrar_historial_publicaciones, name='filtrar_historial_publicaciones'),
    path('filtrar_historial_intercambios/', views.filtrar_historial_intercambios, name='filtrar_historial_intercambios'),
    path('filtrar_historial_donaciones_dinero/', views.filtrar_historial_donaciones_dinero, name='filtrar_historial_donaciones_dinero'),
    path('filtrar_historial_donaciones_producto/', views.filtrar_historial_donaciones_producto, name='filtrar_historial_donaciones_producto'),
]
