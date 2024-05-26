from django.shortcuts import render
from django.http import HttpResponse
from intercambios.models import Intercambio
from sesiones.views import enviar_mail
from django.shortcuts import render, get_object_or_404, redirect
from listados.views import list_exchanges_today
# Create your views here.
def prueba(request, prueba):
    return HttpResponse("<h2>pagina generalh2</h2>")

def listar_intercambios(request):
    return render(request, "intercambios.html")

def confirm_exchange(request, intercambio_id):
    intercambio = get_object_or_404(Intercambio, id=intercambio_id)
    intercambio.estado = "terminado"
    intercambio.save()
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
    return list_exchanges_today(request)