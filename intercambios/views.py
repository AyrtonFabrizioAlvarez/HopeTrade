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
# Create your views here.
def prueba(request, prueba):
    return HttpResponse("<h2>pagina generalh2</h2>")

def listar_intercambios(request):
    return render(request, "intercambios.html")

def confirm_exchange(request, intercambio_id):
    intercambio = get_object_or_404(Intercambio, id=intercambio_id)
    intercambio.estado = "terminado"
    intercambio.save()
    
    publicacionid = intercambio.ofrecimientoId.publicacionId.id
    
    ofrecimientos = Ofrecimiento.objects.filter(publicacionId__id=publicacionid)
    for ofrecimiento in ofrecimientos:
        if intercambio.ofrecimientoId != ofrecimiento:
            enviar_mail(
                "Tu ofrecimiento ya no existe", 
                f"El ofrecimiento que le hiciste a la publicación {ofrecimiento.publicacionId.titulo} ya no existe debido a que ya fue intercambiado", 
                ofrecimiento.usuarioId.email, 
                ""
            )
    
    user1 = intercambio.ofrecimientoId.publicacionId.usuarioId
    user2 = intercambio.ofrecimientoId.usuarioId
    enviar_mail(
        "Valoración", 
        f"Para una mejor seguridad y confiabilidad de los usuarios en nuestra aplicación, nos gustaría que le des una valoración a {user2.personaId.nombre}", 
        user1.email, 
        ""
    )
    enviar_mail(
        "Valoración", 
        f"Para una mejor seguridad y confiabilidad de los usuarios en nuestra aplicación, nos gustaría que le des una valoración a {user1.personaId.nombre}", 
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
    publicacion = intercambio.ofrecimientoId.publicacionId
    publicacion.estado = "disponible"
    publicacion.save()

def partial_absence(request, intercambio_id, user1_id, user2_id):
    cancelar_intercambio(intercambio_id)
    user1 = get_object_or_404(Usuario, id=user1_id)
    user2 = get_object_or_404(Usuario, id=user2_id)
    enviar_mail(
        "Valoración", 
        f"Tu intercambio con {user2.personaId.nombre} ha sido cancelado debido a su ausencia. Para una mejor seguridad y confiabilidad de los usuarios en nuestra aplicación, nos gustaría que le des una valoración a {user2.personaId.nombre}", 
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

def value_user (request):
    return render(request, "intercambios/valorar_usuario.html")