from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from sesiones.models import Persona, Usuario, Ayudante
from datetime import date
from django.shortcuts import get_object_or_404
from .forms import RegistroUsuario, EditarUsuario, EditarPersonaForm, AyudanteForm, PersonaForm
from .models import Usuario, Persona, Ayudante

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
        formularioPersona = EditarPersonaForm(instance=persona)
        return render(request, "editUser.html", {
            'formPerson': formularioPersona,
            'formUser': formularioUsuario
        })
    else:
        usuario = get_object_or_404(Usuario, pk=user_id)
        persona = get_object_or_404(Persona, pk=usuario.personaId.id)
        formularioUsuario = EditarUsuario(request.POST, instance=usuario)
        formularioPersona = EditarPersonaForm(request.POST, instance=persona)
        formularioPersona.save()
        formularioUsuario.save()
        return redirect('/')

def delete_user(request):
    return HttpResponse("vista para eliminar usuario")

def delete_helper(request, helper_id):
    print('entre')
    ayudante = get_object_or_404(Ayudante, pk=helper_id)
    ayudante.nombre_usuario = 'eliminado'
    ayudante.save()
    return redirect('/')


def signup_helper(request):
    if request.method == 'POST':
        persona_form = PersonaForm(request.POST)
        ayudante_form = AyudanteForm(request.POST)
        if persona_form.is_valid() and ayudante_form.is_valid():
            persona = persona_form.save()
            ayudante = ayudante_form.save(commit=False)
            ayudante.personaId = persona
            ayudante.save()
            return redirect('/')
    else:
        persona_form = PersonaForm()
        ayudante_form = AyudanteForm()

    return render(request, 'signup_helper.html', {'persona_form': persona_form, 'ayudante_form': ayudante_form})
    
def list_helpers(request):
    ayudantes = Ayudante.objects.exclude(nombre_usuario='eliminado')
    return render(request, "listadoAyudantes.html", {
        'ayudantes': ayudantes
    })   

def edit_intern(request, helper_id):
    ayudante = get_object_or_404(Ayudante, pk=helper_id)
    persona = get_object_or_404(Persona, pk=ayudante.personaId.id)
    persona_form = EditarPersonaForm(instance=persona)
    if request.method == 'POST':
        nueva_persona_form = EditarPersonaForm(request.POST)
        if nueva_persona_form.is_valid():
            persona = persona_form.save(commit=False)
            persona.nombre = request.POST['nombre']
            persona.apellido = request.POST['apellido']
            persona.contraseña = request.POST['contraseña']
            persona.save()
            return redirect('/')
        else:
            persona_form = nueva_persona_form

    return render(request, 'edit_intern.html', {'formPerson': persona_form})