from django.shortcuts import render
from django.http import HttpResponse
from sesiones.models import Persona, Usuario
from datetime import date
from .forms import RegistroUsuario

# Create your views here.
def signup(request):
    
    print(request.GET)
    return render(request, "signup.html", {
        'form': RegistroUsuario()
    })

def signup_user(request):

    print(request.GET)
    #persona = Persona(nombre="asdasd", apellido="sdddd", contraseña="dddd")
    #persona.save()
    #usuario = Usuario(dni=11222333, email="a@a.com", fecha_nac=date.today(), cant_valoraciones=0, reputacion=0.0, #personaId=persona)
    #usuario.save()
    return HttpResponse("algo para devovler")