from django.urls import path
from .views import donacion_dinero, donacion_producto, ingresar_dni, completar_donacion_existente, completar_donacion_manual, seleccionar_tipo_donacion

urlpatterns = [
    path('ingresar_dni/', ingresar_dni, name='ingresar_dni'),
    path('completar_donacion_existente/<int:usuario_id>/', completar_donacion_existente, name='completar_donacion_existente'),
    path('completar_donacion_manual/<str:dni>/', completar_donacion_manual, name='completar_donacion_manual'),
    path('seleccionar_tipo_donacion/<int:donacion_id>/', seleccionar_tipo_donacion, name='seleccionar_tipo_donacion'),
    path('donacion_dinero/<int:donacion_id>/', donacion_dinero, name='donacion_dinero'),
    path('donacion_producto/<int:donacion_id>/', donacion_producto, name='donacion_producto'),
]