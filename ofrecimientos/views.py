from django.shortcuts import render, redirect, reverse
from sesiones.models import Usuario
from publicaciones.models import Publicacion, Categoria
from intercambios.models import Intercambio
from .models import Ofrecimiento
from .forms import RealizarOfrecimiento, escribir_texto_cancelacion
from intercambios.forms import realizarIntercambio
from sesiones.views import enviar_mail
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
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
                ofrecimiento.estado = 'pendiente'
                ofrecimiento.save()
                subject = f"¡Hola!, te han realizado un ofrecimiento para la publicacion del producto {ofrecimiento.publicacionId.titulo}, saludos!"
                enviar_mail("Tu publicacion de Hope Trade", subject, ofrecimiento.publicacionId.usuarioId.email, ofrecimiento.publicacionId.usuarioId.personaId.nombre)
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
    ofrecimientosPublicacion = Ofrecimiento.objects.all().filter(publicacionId=publicacion).exclude(estado='eliminado')
    categorias = Categoria.objects.all()
    ofrecimiento_info = []
    for ofrecimiento in ofrecimientosPublicacion:
        aux = {
            "id": ofrecimiento.id,
            "articulo": ofrecimiento.articulo,
            "cantidad": ofrecimiento.cantidad,
            "fecha": ofrecimiento.fecha,
            "descripcion": ofrecimiento.descripcion,
            "imagen": None,
            "sucursalId":ofrecimiento.sucursalId,
            "usuarioId":ofrecimiento.usuarioId,
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

    if request.method == 'POST':    
        datos = {
            'estado': 'pendiente',
            'valoracion1': False,
            'valoracion2': False,
            'ofrecimientoId': ofrecimiento.id
        }
        realizar_intercambio_form = realizarIntercambio(data=datos)
    
        if realizar_intercambio_form.is_valid():
            intercambio = realizar_intercambio_form.save(commit=False)
            intercambio.save()
            publicacion = Publicacion.objects.get(id=ofrecimiento.publicacionId.id)
            publicacion.estado = 'aceptada'
            publicacion.save()
            subject = f"¡Hola!, tu ofrecimiento para la publicacion del producto {publicacion.titulo}, a nombre de {publicacion.usuarioId.personaId.nombre} fue aceptado, te esperamos!"
            enviar_mail("Tu ofrecimiento de Hope Trade", subject, ofrecimiento.usuarioId.email, ofrecimiento.usuarioId.personaId.nombre)
            ofrecimiento.estado = 'aceptado'
            ofrecimiento.save()
            messages.success(request, "El ofrecimiento se aceptó exitosamente")
            return redirect( "/publicaciones/listar_publicaciones_sistema/")
        else:
            print('Formulario no válido. Errores:')
            for field, errors in realizar_intercambio_form.errors.items():
                for error in errors:
                    print(f"Error en {field}: {error}")
    return render(request, 'ofrecimientos/aceptar_ofrecimiento.html',{
        'ofrecimiento': ofrecimiento
    })

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
            ofrecimiento.estado = 'eliminado'
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


























############################################################################################################
def ver_mis_ofrecimientos(request, user_id):
    try:
        usuario = Usuario.objects.get(id=user_id)
        ofrecimientos = Ofrecimiento.objects.filter(usuarioId=usuario).exclude(estado='eliminado').exclude(estado='aceptado')
    except ObjectDoesNotExist:
        messages.warning(request, 'No tienes ningún ofrecimiento activo')
    if len(ofrecimientos) == 0:
        messages.warning(request, "No tienes ningún ofrecimiento activo")
    ofrecimientos_final = []
    for ofrecimiento in ofrecimientos:
        ofrecimiento_con_imagen = {
            "id": ofrecimiento.id,
            "articulo": ofrecimiento.articulo,
            "cantidad": ofrecimiento.cantidad,
            'fecha': ofrecimiento.fecha,
            "descripcion": ofrecimiento.descripcion,
            'publicacionId': ofrecimiento.publicacionId,
            "imagen": None,
            "sucursalId":ofrecimiento.sucursalId,
        }
        if ofrecimiento.imagen:
            imagen = ofrecimiento.imagen.decode("utf-8")
            ofrecimiento_con_imagen["imagen"] = imagen
        ofrecimientos_final.append(ofrecimiento_con_imagen)
    return render(request, 'ofrecimientos/ver_mis_ofrecimientos.html', {
        'ofrecimientos': ofrecimientos_final,
    })
    
def eliminar_ofrecimiento(request, ofrecimiento_id):
    ofrecimiento = Ofrecimiento.objects.get(id=ofrecimiento_id)
    if request.method == "POST":
        ofrecimiento.estado = 'eliminado'
        ofrecimiento.save()
        messages.success(request, "El ofrecimiento se eliminó exitosamente")
        return redirect('ofrecimientos:ver_mis_ofrecimientos', user_id=request.session['rol_id'])
    ofrecimiento.imagen = ofrecimiento.imagen.decode("utf-8")
    return render(request, 'ofrecimientos/eliminar_ofrecimiento.html', { 'ofrecimiento': ofrecimiento })
############################################################################################################
    

