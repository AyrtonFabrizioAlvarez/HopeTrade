from django.urls import path
from . import views

urlpatterns = [
    path('publicaciones_sistema/', views.historial_publicaciones_sistema, name='historial_publicaciones_sistema'),
    path('intercambios_sistema/', views.historial_intercambios_sistema, name='historial_intercambios_sistema'),
    path('donaciones_sistema/', views.historial_donaciones_sistema, name='historial_donaciones_sistema'),
    path('publicaciones_usuario/<int:user_id>/', views.historial_publicaciones_usuario, name='historial_publicaciones_usuario'),
    path('intercambios_usuario/<int:user_id>/', views.historial_intercambios_usuario, name='historial_intercambios_usuario'),
]
