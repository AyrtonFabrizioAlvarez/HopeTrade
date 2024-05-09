from django.shortcuts import render, redirect
from django.http import HttpResponse
from sesiones.models import Persona, Usuario
from datetime import date
from django.shortcuts import get_object_or_404
from .forms import RegistroUsuario, EditarUsuario, EditarPersona
from .models import Usuario, Persona

# Create your views here.
def signup(request):
    if request.method == "GET":
        return render(request, "signup.html", {
            'form': RegistroUsuario()
        })
    else:
        persona = Persona.objects.create(nombre=request.POST['nombre'], apellido=request.POST['apellido'], contraseña=request.POST['contraseña'])
        persona.save()
        usuario = Usuario.objects.create(dni=request.POST['dni'], email=request.POST['email'], fecha_nac=date.today(), cant_valoraciones=0, reputacion=0.0, personaId=persona)
        usuario.save()
        return redirect('/')
  
  
def list_users(request):
    usuarios = Usuario.objects.all()
    return render(request, "listadoUsuarios.html", {
        'usuarios': usuarios
    })      

def edit_user(request, user_id):
    if request.method == "GET":
        usuario = get_object_or_404(Usuario, pk=user_id)
        persona = get_object_or_404(Persona, pk=usuario.personaId.id)
        formularioUsuario = EditarUsuario(instance=usuario)
        formularioPersona = EditarPersona(instance=persona)
        return render(request, "editUser.html", {
            'formPerson': formularioPersona,
            'formUser': formularioUsuario
        })
    else:
        print('aca se haria la edicion de la persona/usuario')

def delete_user(request):
    return HttpResponse("vista para eliminar usuario")