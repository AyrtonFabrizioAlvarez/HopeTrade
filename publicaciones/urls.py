from django.urls import path
from publicaciones import views as publicaciones

urlpatterns = [
    path('realizar_publicacion/', publicaciones.realizar_publicacion, name='realizar_publicacion'),
    path('listar_publicaciones_sistema/', publicaciones.listar_publicaciones_sistema),
    path('listar_publicaciones_usuario/', publicaciones.listar_publicaciones_usuario),
    path('realizar_comentario/', publicaciones.realizar_comentario),
    path('cancelar/', publicaciones.cancelar_operacion, name='cancelar_operacion'),
    path('seleccionar_publicacion/<int:publicacion_id>/', publicaciones.seleccionar_publicacion, name='seleccionar_publicacion'),
    path('seleccionar_publicacion/<int:publicacion_id>/realizar_comentario/', publicaciones.realizar_comentario, name='realizar_comentario'),
]


