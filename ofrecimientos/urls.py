from django.urls import path
from . import views

app_name = 'ofrecimientos'

urlpatterns = [
    path('publicaciones/realizar_ofrecimiento/', views.realizar_ofrecimiento),
    path('seleccionar_publicacion/<int:publicacion_id>/realizar_ofrecimiento/', views.realizar_ofrecimiento, name='realizar_ofrecimiento'),
    path('ver_ofrecimientos/<int:publicacion_id>', views.ver_ofrecimientos, name='ver_ofrecimientos'),
]