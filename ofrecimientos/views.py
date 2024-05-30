from django.shortcuts import render, redirect, reverse
from sesiones.models import Usuario
from publicaciones.models import Publicacion, Categoria
from intercambios.models import Intercambio
from .models import Ofrecimiento
from .forms import RealizarOfrecimiento, escribir_texto_cancelacion
from intercambios.forms import realizarIntercambio
from sesiones.views import enviar_mail
from django.contrib import messages
from datetime import datetime
import base64

# Create your views here.
def realizar_ofrecimiento(request, publicacion_id):
    if request.method == "POST":
        realizar_ofrecimiento_form = RealizarOfrecimiento(request.POST, request.FILES)
        if realizar_ofrecimiento_form.is_valid():
            try:
                ofrecimiento = realizar_ofrecimiento_form.save(commit=False)
                usuarioId = request.session.get('rol_id')
                ofrecimiento.usuarioId = Usuario.objects.get(id=usuarioId)
                ofrecimiento.publicacionId = Publicacion.objects.get(id=publicacion_id)
                imagen=(
                    base64.b64encode(realizar_ofrecimiento_form.cleaned_data["imagen"].read())
                    if realizar_ofrecimiento_form.cleaned_data["imagen"]
                    else realizar_ofrecimiento_form.cleaned_data["imagen"]
                )
                ofrecimiento.imagen = imagen
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
        'realizar_ofrecimiento_form': realizar_ofrecimiento_form
    })

def ver_ofrecimientos(request, publicacion_id):
    publicacion = Publicacion.objects.get(id=publicacion_id)
    ofrecimientosPublicacion = Ofrecimiento.objects.all().filter(publicacionId=publicacion).exclude(estado='rechazado')
    categorias = Categoria.objects.all()
    ofrecimiento_info = []
    for ofrecimiento in ofrecimientosPublicacion:
        aux = {
            "id": ofrecimiento.id,
            "articulo": ofrecimiento.articulo,
            "cantidad": ofrecimiento.cantidad,
            "descripcion": ofrecimiento.descripcion,
            "imagen": None,
        }
        if ofrecimiento.imagen:
            imagen = ofrecimiento.imagen.decode("utf-8")
            aux["imagen"] = imagen
        ofrecimiento_info.append(aux)
    if len(ofrecimientosPublicacion) == 0:
        messages.warning(request, 'Esta publicación no tiene ofrecimientos')
    return render(request, "ofrecimientos/ver_ofrecimientos.html", {
        'ofrecimientosPublicacion': ofrecimiento_info,
        'categorias': categorias,
    })

def aceptar_ofrecimiento(request, ofrecimiento_id):
    ofrecimiento = Ofrecimiento.objects.get(id=ofrecimiento_id)
    datos = {'estado': 'pendiente',
            'ofrecimientoId': ofrecimiento}
    if request.method == 'POST':
        realizar_intercambio_form = realizarIntercambio(request.POST,initial=datos)
        if realizar_intercambio_form.is_valid():
            intercambio = realizar_intercambio_form.save(commit=False)
            intercambio.save()
            publicacion = Publicacion.objects.get(id=ofrecimiento.publicacionId)
            publicacion.estado = 'aceptada'
            subject = f"¡Hola!, tu ofrecimiento para la publicacion del producto {publicacion.titulo}, a nombre de {publicacion.usuarioId.personaId.nombre} fue aceptado, te esperamos!"
            enviar_mail("Tu ofrecimiento de Hope Trade", subject, ofrecimiento.usuarioId.email, ofrecimiento.usuarioId.personaId.nombre)
            ofrecimiento.estado = 'aceptado'
            messages.success(request, "El ofrecimiento se aceptó exitosamente")
            return redirect( "/publicaciones/listar_publicaciones_sistema/")
    else:
        realizar_intercambio_form = realizarIntercambio(initial=datos)
    return render(request, 'ver_ofrecimientos.html', {'form': realizar_intercambio_form, 'ofrecimiento': ofrecimiento})

def rechazar_ofrecimiento(request, ofrecimiento_id):
    ofrecimiento = Ofrecimiento.objects.get(id=ofrecimiento_id)
    publicacion = Publicacion.objects.get(id=ofrecimiento.publicacionId.id)
    if request.method == 'POST':
        form = escribir_texto_cancelacion(request.POST)
        if form.is_valid():
            texto = form.cleaned_data['texto']
            if not texto.strip():
                subject = f"¡Hola!, tu ofrecimiento para la publicacion del producto {publicacion.titulo}, a nombre de {publicacion.usuarioId.personaId.nombre} fue rechazado."
            else:
                subject = f"¡Hola!, tu ofrecimiento para la publicacion del producto {publicacion.titulo}, a nombre de {publicacion.usuarioId.personaId.nombre} fue rechazado. La razón: {texto}"
            enviar_mail("Tu ofrecimiento de Hope Trade", subject, ofrecimiento.usuarioId.email, ofrecimiento.usuarioId.personaId.nombre)
            ofrecimiento.estado = 'rechazado'
            ofrecimiento.save()
            messages.success(request, "El ofrecimiento se rechazó exitosamente")
            url = reverse('ofrecimientos:ver_ofrecimientos', kwargs={'publicacion_id': publicacion.id})
            return redirect(url)
    else:
        form = escribir_texto_cancelacion()
    return render(request, 'ofrecimientos/rechazar_ofrecimiento.html',{
        'form': form ,
        'publicacionId': publicacion.id,
    })

def cancelar_operacion(request, publicacion_id):
    ruta = "/ofrecimientos/ver_ofrecimientos/" + str(publicacion_id)
    return redirect(ruta)

