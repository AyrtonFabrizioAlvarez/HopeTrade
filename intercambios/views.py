from django.shortcuts import render
from django.http import HttpResponse
from intercambios.models import Intercambio
from ofrecimientos.models import Ofrecimiento
from publicaciones.models import Publicacion
from sesiones.models import Usuario
from sesiones.views import enviar_mail
from django.shortcuts import render, get_object_or_404, redirect
from listados.views import list_exchanges_today
from .forms import escribir_texto_cancelacion
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from historiales.models import Historial, IntercambioHistorial, PublicacionHistorial
import datetime

# Create your views here.
def prueba(request, prueba):
    return HttpResponse("<h2>pagina generalh2</h2>")

def listar_intercambios(request):
    return render(request, "intercambios.html")

def confirm_exchange(request, intercambio_id):
    intercambio = get_object_or_404(Intercambio, id=intercambio_id)
    intercambio.estado = "confirmado"
    intercambio.save()
    #SE CREA UN LOG EN EL HISTORIAL DE INTERCAMBIOS
    historial = Historial.objects.create(estado="confirmado", fecha=datetime.datetime.now())
    historial_intercambio = IntercambioHistorial.objects.create(intercambioId=intercambio, historialId=historial)
    
    publicacionid = intercambio.ofrecimientoId.publicacionId.id
    publicacion = intercambio.ofrecimientoId.publicacionId
    publicacion.estado = "finalizada"
    publicacion.save()
    #SE CREA UN LOG EN EL HISTORIAL DE PUBLICACIONES
    historial = Historial.objects.create(estado="finalizada", fecha=datetime.datetime.now())
    historial_publicacion = PublicacionHistorial.objects.create(publicacionId=publicacion, historialId=historial)
    
    ofrecimientos = Ofrecimiento.objects.filter(publicacionId__id=publicacionid)
    for ofrecimiento in ofrecimientos:
        if intercambio.ofrecimientoId.id != ofrecimiento.id:
            enviar_mail(
                "Tu ofrecimiento ya no existe", 
                f"El ofrecimiento que le hiciste a la publicación {ofrecimiento.publicacionId.titulo} ya no existe debido a que ya fue intercambiado", 
                ofrecimiento.usuarioId.email, 
                ""
            )
            ofrecimiento.estado = "eliminado"
            ofrecimiento.save()
    user1 = intercambio.ofrecimientoId.publicacionId.usuarioId
    user2 = intercambio.ofrecimientoId.usuarioId
    link1 = f"http://127.0.0.1:8000/intercambios/value_user/{intercambio_id}/{user1.id}/{user2.id}/{1}"
    link2 = f"http://127.0.0.1:8000/intercambios/value_user/{intercambio_id}/{user2.id}/{user1.id}/{2}"
    enviar_mail(
        "Valoración", 
        f"Para una mejor seguridad y confiabilidad de los usuarios en nuestra aplicación, nos gustaría que le des una valoración a {user2.personaId.nombre} a traves del siguiente link: {link1}", 
        user1.email, 
        ""
    )
    enviar_mail(
        "Valoración", 
        f"Para una mejor seguridad y confiabilidad de los usuarios en nuestra aplicación, nos gustaría que le des una valoración a {user1.personaId.nombre} a traves del siguiente link: {link2}", 
        user2.email, 
        ""
    )
    
    messages.success(request, 'Se confirmó el intercambio y enviaron los mails exitosamente')
    return list_exchanges_today(request)

def cancel_exchange(request, intercambio_id):
    intercambio = get_object_or_404(Intercambio, id=intercambio_id)
    return render(request, "intercambios/cancelar_intercambio.html", {"intercambio": intercambio})

def cancel_exchange_partial_absence(request, intercambio_id, user1_id, user2_id):
    intercambio = get_object_or_404(Intercambio, id=intercambio_id)
    return render(request, "intercambios/inasistencia_parcial.html", {"intercambio": intercambio})


def cancelar_intercambio(intercambio_id):
    intercambio = get_object_or_404(Intercambio, id=intercambio_id)
    intercambio.estado = "cancelado"
    intercambio.save()
    #SE CREA UN LOG EN EL HISTORIAL DE INTERCAMBIOS
    historial = Historial.objects.create(estado="cancelado", fecha=datetime.datetime.now())
    IntercambioHistorial.objects.create(intercambioId=intercambio, historialId=historial)
    
    publicacion = intercambio.ofrecimientoId.publicacionId
    publicacion.estado = "disponible"
    publicacion.save()
    #SE CREA UN LOG EN EL HISTORIAL DE PUBLICACIONES
    historial = Historial.objects.create(estado="disponible", fecha=datetime.datetime.now())
    PublicacionHistorial.objects.create(publicacionId=publicacion, historialId=historial)
    
    ofrecimiento = intercambio.ofrecimientoId
    ofrecimiento.estado = "rechazado"
    ofrecimiento.save()

def partial_absence(request, intercambio_id, user1_id, user2_id):
    cancelar_intercambio(intercambio_id)
    user1 = get_object_or_404(Usuario, id=user1_id)
    user2 = get_object_or_404(Usuario, id=user2_id)
    link1 = f"http://127.0.0.1:8000/intercambios/value_user/{intercambio_id}/{user1.id}/{user2.id}/{1}"
    enviar_mail(
        "Valoración", 
        f"Tu intercambio con {user2.personaId.nombre} ha sido cancelado debido a su ausencia. Para una mejor seguridad y confiabilidad de los usuarios en nuestra aplicación, nos gustaría que le des una valoración a {user2.personaId.nombre} en el siguiente link: {link1}", 
        user1.email, 
        ""
    )
    enviar_mail(
        "Intercambio Cancelado", 
        f"Tu intercambio con {user1.personaId.nombre} ha sido cancelado debido a tu ausencia ", 
        user2.email, 
        ""
    )
    messages.success(request, 'Se canceló el intercambio y enviaron los mails exitosamente')
    return list_exchanges_today(request)

def total_absence(request, intercambio_id, user1_id, user2_id):
    cancelar_intercambio(intercambio_id)
    enviar_mails_cancelacion(user1_id, user2_id, "mutua ausencia")
    messages.success(request, 'Se canceló el intercambio y enviaron los mails exitosamente')
    return list_exchanges_today(request)

def other(request, intercambio_id, user1_id, user2_id):
    if request.method == "GET":
        return render(request, "intercambios/otro.html", {"form": escribir_texto_cancelacion()})
    elif request.method == "POST":
        form = escribir_texto_cancelacion(request.POST)
        if form.is_valid():
            razon = form.cleaned_data.get('razon')
            cancelar_intercambio(intercambio_id)
            enviar_mails_cancelacion(user1_id, user2_id, razon)
            messages.success(request, 'Se canceló el intercambio y enviaron los mails exitosamente')
            return list_exchanges_today(request)
        else:
            return render(request, "intercambios/otro.html", {"form": form})

def enviar_mails_cancelacion(user1_id, user2_id, razon):
    user1 = get_object_or_404(Usuario, id=user1_id)
    user2 = get_object_or_404(Usuario, id=user2_id)
    enviar_mail(
        "Intercambio Cancelado", 
        f"Tu intercambio con {user2.personaId.nombre} ha sido cancelado debido a {razon} ", 
        user1.email, 
        ""
    )
    enviar_mail(
        "Intercambio Cancelado", 
        f"Tu intercambio con {user1.personaId.nombre} ha sido cancelado debido a {razon} ", 
        user2.email, 
        ""
    )

def guardar_valoracion(request, user2):
    rating = int(request.POST.get('rating', 0))
    user2.reputacion = (user2.reputacion + rating) / (user2.cant_valoraciones + 1)
    user2.cant_valoraciones = user2.cant_valoraciones + 1
    user2.save()
    messages.success(request, 'Tu valoración se envió exitosamente')

def value_user (request, intercambio_id, user1_id, user2_id, num):
    user2 = get_object_or_404(Usuario, id=user2_id)
    if request.method == "GET":
        return render(request, "intercambios/valorar_usuario.html", {"intercambio_id": intercambio_id, "user1_id": user1_id, "user2_id": user2_id, "num": num})
    elif request.method == 'POST':
        intercambio = get_object_or_404(Intercambio, id=intercambio_id)
        if num == 1 and intercambio.valoracion1== False:
            guardar_valoracion(request, user2)
            intercambio.valoracion1 = True
            intercambio.save()
        elif num == 2 and intercambio.valoracion2 == False:
            guardar_valoracion(request, user2)
            intercambio.valoracion2 = True
            intercambio.save()
        else:
            messages.error(request, "Ya has realizado esta valoracion")
        return redirect("/")  

def listar_intercambios(request, user_id):
    if(request.session['rol'] == 'administrador'):
        intercambios = Intercambio.objects.all()
    else:
        usuario = Usuario.objects.get(id=user_id)
        publicaciones_usuario = Publicacion.objects.filter(usuarioId=usuario)
        ofrecimientos_recibidos = Ofrecimiento.objects.filter(publicacionId__in = publicaciones_usuario)
        ofrecimientos_usuario = Ofrecimiento.objects.filter(usuarioId=user_id)
        intercambios = Intercambio.objects.filter(Q(ofrecimientoId__in = ofrecimientos_usuario) | Q(ofrecimientoId__in=ofrecimientos_recibidos))
    
    if len(intercambios) == 0:
        messages.warning(request, 'No existen intercambios')
    return render(request, "intercambios/listar_intercambios.html",{'intercambios': intercambios})



def filtrar_intercambios(request):
    intercambios = Intercambio.objects.all()
    estado = request.POST.get('estado')
    estado_seleccionado = None
    if estado != 'Estado' and estado != None:
        intercambios = intercambios.filter(estado=estado)
        estado_seleccionado = estado
    if len(intercambios) == 0:
        messages.warning(request, f'No existen intercambios para el filtro seleccionado')
    return render(request, "intercambios/listar_intercambios.html", {
        'intercambios': intercambios,
        'estado_seleccionado':estado_seleccionado
    })



def actualizar_sistema(request):
    hoy = timezone.now().date()
    ofrecimientos = Ofrecimiento.objects.filter(fecha__date=hoy).filter(estado = "pendiente")
    for ofrecimiento in ofrecimientos:
        ofrecimiento.estado = "eliminado"
        ofrecimiento.save()
        enviar_mail(
        "Valoración", 
        f"Tu ofrecimiento {ofrecimiento.articulo} ha sido eliminado debido a la expiración de la fecha", 
        ofrecimiento.usuarioId.email, 
        ""    
        )
    messages.success(request, 'Se ha actualizado el sistema correctamente')
    return list_exchanges_today(request)