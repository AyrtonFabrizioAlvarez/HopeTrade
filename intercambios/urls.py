from django.urls import path
from . import views

urlpatterns = [
    path('cancelar_intercambio/<int:intercambio_id>/', views.cancel_exchange, name='cancelar_intercambio'),
    path('partial_absence/<int:intercambio_id>/<int:user1_id>/<int:user2_id>/', views.cancel_exchange_partial_absence, name='inasistencia_parcial'),
    path('partial_absence/<int:intercambio_id>/<int:user1_id>/<int:user2_id>/enviarmails/', views.partial_absence, name='inasistencia_parcial_enviarmails'),
    path('total_absence/<int:intercambio_id>/<int:user1_id>/<int:user2_id>/', views.total_absence, name='inasistencia_total'),
    path('other/<int:intercambio_id>/<int:user1_id>/<int:user2_id>/', views.other, name='otro'),
    path('value_user/<int:intercambio_id>/<int:user1_id>/<int:user2_id>/', views.value_user, name='valorar_usuario'),
    path('listar_intercambios/<int:user_id>/', views.listar_intercambios, name='listar_intercambios'),
    path('filtrar_intercambios/', views.filtrar_intercambios, name='filtrar_intercambios')
]
