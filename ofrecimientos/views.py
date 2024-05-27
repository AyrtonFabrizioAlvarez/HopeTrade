from django.shortcuts import render, redirect
from sesiones.models import Usuario
from publicaciones.models import Publicacion, Categoria
from .models import Ofrecimiento
from .forms import RealizarOfrecimiento
from django.contrib import messages
from datetime import datetime

# Create your views here.
def realizar_ofrecimiento(request, publicacion_id):
    if request.method == "POST":
        realizar_ofrecimiento_form = RealizarOfrecimiento(request.POST)
        if realizar_ofrecimiento_form.is_valid():
            try:
                ofrecimiento = realizar_ofrecimiento_form.save(commit=False)
                usuarioId = request.session.get('rol_id')
                ofrecimiento.usuarioId = Usuario.objects.get(id=usuarioId)
                ofrecimiento.publicacionId = Publicacion.objects.get(id=publicacion_id)
                ofrecimiento.save()
                messages.success(request, "El ofrecimiento se creó exitosamente")
                ruta = "/publicaciones/seleccionar_publicacion/" + str(publicacion_id)
                return redirect(ruta)
            except:
                return render(request, "ofrecimientos/realizar_ofrecimiento.html", {
                    'form': RealizarOfrecimiento(),
                    "error": 'algo salió mal'
                })
    else:
        realizar_ofrecimiento_form = RealizarOfrecimiento()
    return render(request, "ofrecimientos/realizar_ofrecimiento.html", {
        'form': RealizarOfrecimiento()
    })

def ver_ofrecimientos(request, publicacion_id):
    publicacion = Publicacion.objects.get(id=publicacion_id)
    ofrecimientosPublicacion = Ofrecimiento.objects.all().filter(publicacionId=publicacion)
    categorias = Categoria.objects.all()
    if len(ofrecimientosPublicacion) == 0:
        messages.warning(request, 'Esta publicación no tiene ofrecimientos')
    return render(request, "ofrecimientos/ver_ofrecimientos.html", {
        'ofrecimientosPublicacion': ofrecimientosPublicacion,
        'categorias': categorias,
    })

