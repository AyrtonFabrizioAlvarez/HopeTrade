from django.shortcuts import render
from .models import Historial, IntercambioHistorial, PublicacionHistorial
from publicaciones.models import Publicacion
from intercambios.models import Intercambio
from donaciones.models import Donacion, Donacion_din, Donacion_prod
from sesiones.models import Usuario
from django.core import exceptions
from django.contrib import messages
from listados.models import Categoria
from datetime import datetime
import pytz

def historial_publicaciones_sistema(request):

    if request.session["rol"] != "administrador":
        publicaciones = Publicacion.objects.filter(usuarioId=request.session["rol_id"])
        historial = PublicacionHistorial.objects.filter(publicacionId__in=publicaciones)
    else:
        historial = PublicacionHistorial.objects.all()
    categorias = Categoria.objects.all()

    if len(historial) == 0:
        messages.warning(request, 'No existen publicaciones en el sistema')
    return render(request, 'historiales/historial_publicaciones.html',
                  {
                      "historial":historial,
                      "categorias":categorias,
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
    return render(request, 'historiales/historial_donaciones.html')

def historial_donaciones_dinero_sistema(request):
    if request.session["rol"] == "administrador":
        donaciones = Donacion_din.objects.all() 
    else:
        donaciones = Donacion_din.objects.filter(donacionId__usuarioId__id=request.session["rol_id"])
    categorias = Categoria.objects.all()
    if len(donaciones) == 0:
        messages.warning(request, f'No existen donaciones en el sistema')

    return render(request, 'historiales/historial_donaciones.html',
                  {
                      'donaciones':donaciones,
                      'categorias':categorias,
                  }
    )
def historial_donaciones_productos_sistema(request):
    if request.session["rol"] == "administrador":
        donaciones = Donacion_prod.objects.all()
    else:
        donaciones = Donacion_prod.objects.filter(donacionId__usuarioId__id=request.session["rol_id"])
    categorias = Categoria.objects.all()
    if len(donaciones) == 0:
        messages.warning(request, f'No existen donaciones en el sistema')
    return render(request, 'historiales/historial_donaciones.html',
                  {
                      'donaciones':donaciones,
                      'categorias':categorias,
                  }
    )


def historial_publicaciones_usuario(request, user_id):
    try:
        publicaciones = Publicacion.objects.filter(usuarioId=user_id)
        historial = PublicacionHistorial.objects.filter(publicacionId__in=publicaciones)
        categorias = Categoria.objects.all()
    except exceptions.ObjectDoesNotExist:
        historial = []
    if len(historial) == 0:
        messages.warning(request, f'No existen publicaciones en el sistema')
    return render(request, 'historiales/historial_publicaciones.html', 
                  {
                      'historial':historial,
                      'categorias':categorias,
                  })

def historial_intercambios_usuario(request, user_id):
    try:
        intercambios_usuario = Intercambio.objects.filter(ofrecimientoId__usuarioId=user_id) | Intercambio.objects.filter(ofrecimientoId__publicacionId__usuarioId=user_id)
        historial = IntercambioHistorial.objects.filter(intercambioId__in=intercambios_usuario)
    except exceptions.ObjectDoesNotExist:
        messages.warning(request, 'No existen intercambios en el sistema')
    if len(historial) == 0:
        messages.warning(request, f'No existen intercambios en el sistema')
    return render(request, 'historiales/historial_intercambios.html', 
                  {
                      'historial':historial,
                  })
    
def filtrar_historial_publicaciones(request):
    historial = PublicacionHistorial.objects.all()
    if request.session['rol'] != "administrador":
        historial = historial.filter(publicacionId__usuarioId__id=request.session['rol_id'])
    categorias = Categoria.objects.all()
    categoria = request.POST.get('categoria')
    categoria_seleccionada = None
    estado = request.POST.get('estado')
    estado_seleccionado = None
    if categoria != 'Categoria' and categoria != None:
        if categoria.isdigit():
            historial = historial.filter(publicacionId__categoriaId__id=categoria)
            categoria_seleccionada = Categoria.objects.get(id=categoria)
        else:
            categoria_seleccionada = Categoria.objects.get(titulo=categoria)
            historial = historial.filter(publicacionId__categoriaId__id=categoria_seleccionada.id)
    if estado != 'Estado' and estado != None:
        historial = historial.filter(historialId__estado=estado)
        estado_seleccionado = estado
    if len(historial) == 0:
        messages.warning(request, f'No existen publicaciones para el filtro seleccionado')
    return render(request, "historiales/historial_publicaciones.html", {
        'historial': historial,
        'categorias': categorias,
        'categoria_seleccionada':categoria_seleccionada,
        'estado_seleccionado':estado_seleccionado
    })

def filtrar_historial_intercambios(request):
    historial = IntercambioHistorial.objects.all()
    fecha_desde = request.POST['fecha_desde']
    fecha_hasta = request.POST['fecha_hasta']
    categorias = Categoria.objects.all()
    categoria = request.POST.get('categoria')
    categoria_seleccionada = None
    estado = request.POST.get('estado')
    estado_seleccionado = None
    if request.session['rol'] != "administrador":
        intercambios_usuario = Intercambio.objects.filter(ofrecimientoId__usuarioId=request.session['rol_id']) | Intercambio.objects.filter(ofrecimientoId__publicacionId__usuarioId=request.session['rol_id'])
        historial = IntercambioHistorial.objects.filter(intercambioId__in=intercambios_usuario)
    if categoria != 'Categoria' and categoria != None:
        if categoria.isdigit():
            historial = historial.filter(intercambioId__ofrecimientoId__publicacionId__categoriaId__id=categoria)
            categoria_seleccionada = Categoria.objects.get(id=categoria)
        else:
            categoria_seleccionada = Categoria.objects.get(titulo=categoria)
            historial = historial.filter(intercambioId__ofrecimientoId__publicacionId__categoriaId__id=categoria_seleccionada.id)
    if estado != 'Estado' and estado != None:
        historial = historial.filter(historialId__estado=estado)
        estado_seleccionado = estado
    if fecha_desde:
        timezone = pytz.UTC
        fecha_desde_formateada = timezone.localize(datetime.strptime(fecha_desde, '%Y-%m-%dT%H:%M'))
        historial = historial.filter(intercambioId__ofrecimientoId__fecha__gte=fecha_desde_formateada)
    if fecha_hasta:
        timezone = pytz.UTC
        fecha_hasta_formateada = timezone.localize(datetime.strptime(fecha_hasta, '%Y-%m-%dT%H:%M'))
        historial = historial.filter(intercambioId__ofrecimientoId__fecha__lte=fecha_hasta_formateada)
    if len(historial) == 0:
        messages.warning(request, f'No existen intercambios para el filtro seleccionado')
    return render(request, "historiales/historial_intercambios.html", {
        'historial': historial,
        'categorias': categorias,
        'categoria_seleccionada':categoria_seleccionada,
        'estado_seleccionado':estado_seleccionado,
        'fecha_desde_seleccionada':fecha_desde,
        'fecha_hasta_seleccionada':fecha_hasta,
    })
    
def filtrar_historial_donaciones_dinero(request):
    forma_pago = request.POST.get('forma de pago')
    forma_pago_seleccionada = None
    fecha_desde = request.POST['fecha_desde']
    fecha_hasta = request.POST['fecha_hasta']
    donaciones = Donacion.objects.all()
    
    if request.session["rol"] == "administrador":
        donaciones = Donacion_din.objects.all()
    else:
        donaciones = Donacion_din.objects.filter(donacionId__usuarioId__id=request.session["rol_id"])
    if forma_pago != 'Forma de Pago' and forma_pago != None:
        forma_pago_seleccionada = forma_pago
        donaciones = donaciones.filter(forma_pago=forma_pago)
    
    if fecha_desde:
        timezone = pytz.UTC
        fecha_desde_formateada = timezone.localize(datetime.strptime(fecha_desde, '%Y-%m-%d'))
        donaciones = donaciones.filter(donacionId__fecha__gte=fecha_desde_formateada)
    if fecha_hasta:
        timezone = pytz.UTC
        fecha_hasta_formateada = timezone.localize(datetime.strptime(fecha_hasta, '%Y-%m-%d'))
        donaciones = donaciones.filter(donacionId__fecha__lte=fecha_hasta_formateada)
    if len(donaciones) == 0:
        messages.warning(request, f'No existen donaciones para el filtro seleccionado')
    
    return render(request, "historiales/historial_donaciones.html", {
        'donaciones': donaciones,
        'forma_pago_seleccionada':forma_pago_seleccionada,
        'fecha_desde_seleccionada':fecha_desde,
        'fecha_hasta_seleccionada':fecha_hasta,
    })



def filtrar_historial_donaciones_producto(request):
    fecha_desde = request.POST['fecha_desde']
    fecha_hasta = request.POST['fecha_hasta']
    donaciones = Donacion.objects.all()
    
    if request.session["rol"] == "administrador":
        donaciones = Donacion_prod.objects.all()
    else:
        donaciones = Donacion_prod.objects.filter(donacionId__usuarioId__id=request.session["rol_id"])
    print(len(donaciones))
    if fecha_desde:
        timezone = pytz.UTC
        fecha_desde_formateada = timezone.localize(datetime.strptime(fecha_desde, '%Y-%m-%d'))
        donaciones = donaciones.filter(donacionId__fecha__gte=fecha_desde_formateada)
    print(len(donaciones))
    if fecha_hasta:
        timezone = pytz.UTC
        fecha_hasta_formateada = timezone.localize(datetime.strptime(fecha_hasta, '%Y-%m-%d'))
        donaciones = donaciones.filter(donacionId__fecha__lte=fecha_hasta_formateada)
    print(len(donaciones))

    if len(donaciones) == 0:
        print('entre porque hay 0 donaciones que mostrar')
        messages.warning(request, f'No existen donaciones para el filtro seleccionado')
    
    return render(request, "historiales/historial_donaciones.html", {
        'donaciones': donaciones,
        'fecha_desde_seleccionada':fecha_desde,
        'fecha_hasta_seleccionada':fecha_hasta,
    })
