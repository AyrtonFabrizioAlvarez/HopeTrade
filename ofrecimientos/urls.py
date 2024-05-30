from django.urls import path
from . import views

app_name = 'ofrecimientos'

urlpatterns = [
    path('publicaciones/realizar_ofrecimiento/', views.realizar_ofrecimiento),
    path('seleccionar_publicacion/<int:publicacion_id>/realizar_ofrecimiento/', views.realizar_ofrecimiento, name='realizar_ofrecimiento'),
    path('ver_ofrecimientos/<int:publicacion_id>', views.ver_ofrecimientos, name='ver_ofrecimientos'),
    path('aceptar_ofrecimiento/<int:ofrecimiento_id>', views.aceptar_ofrecimiento, name='aceptar_ofrecimiento'),
    path('rechazar_ofrecimiento/<int:ofrecimiento_id>', views.rechazar_ofrecimiento, name='rechazar_ofrecimiento'),
    path('cancelar_operacion/<int:publicacion_id>', views.cancelar_operacion, name='cancelar_operacion'),
]