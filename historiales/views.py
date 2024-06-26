from django.shortcuts import render
from .models import Historial, IntercambioHistorial, PublicacionHistorial
from publicaciones.models import Publicacion
from intercambios.models import Intercambio
from donaciones.models import Donacion, Donacion_din, Donacion_prod
from sesiones.models import Usuario
from django.core import exceptions
from django.contrib import messages

def historial_publicaciones_sistema(request):

    historial = PublicacionHistorial.objects.all()
    if len(historial) == 0:
        messages.warning(request, 'No existen publicaciones en el sistema')
    return render(request, 'historiales/historial_publicaciones.html',
                  {
                      "historial":historial,
                  })

def historial_intercambios_sistema(request):
    historial = IntercambioHistorial.objects.all()
    if len(historial) == 0:
        messages.warning(request, 'No existen intercambios en el sistema')
    return render(request, 'historiales/historial_intercambios.html',
                  {
                      "historial":historial,
                  })

def historial_donaciones_sistema(request):
    return True

def historial_publicaciones_usuario(request, user_id):
    try:
        publicaciones = Publicacion.objects.filter(usuarioId=user_id)
        historial = PublicacionHistorial.objects.filter(publicacionId__in=publicaciones)
    except exceptions.ObjectDoesNotExist:
        historial = []
        messages.warning(request, 'No existen publicaciones en el sistema')
    return render(request, 'historiales/historial_publicaciones.html', 
                  {
                      'historial':historial,
                  })

def historial_intercambios_usuario(request, user_id):
    try:
        intercambios_usuario = Intercambio.objects.filter(ofrecimientoId__usuarioId=user_id) | Intercambio.objects.filter(ofrecimientoId__publicacionId__usuarioId=user_id)
        historial = IntercambioHistorial.objects.filter(intercambioId__in=intercambios_usuario)
    except exceptions.ObjectDoesNotExist:
        messages.warning(request, 'No existen intercambios en el sistema')
    return render(request, 'historiales/historial_intercambios.html', 
                  {
                      'historial':historial,
                  })
