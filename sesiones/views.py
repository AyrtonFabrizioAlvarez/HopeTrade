from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import PersonaForm, UsuarioForm, AyudanteForm, EditarUsuarioForm, EditarPersonaForm, EditarAyudanteForm
from .models import Persona, Usuario, Ayudante

# Create your views here.
def ver_landing_page(request):
    return render(request, 'landingPage.html')

def signup(request):
    if request.method == "GET":
        persona_form = PersonaForm()
        usuario_form = UsuarioForm()
        return render(request, "sesiones/signup.html", {
            'form_persona': persona_form,
            'form_usuario': usuario_form
        })
    else:
        print(request.POST)
        persona_form = PersonaForm(request.POST)
        usuario_form = UsuarioForm(request.POST)
        print(persona_form.is_valid())
        print(usuario_form.is_valid())
        if persona_form.is_valid() and usuario_form.is_valid():
            print('es valido')
            persona = persona_form.save()
            usuario = usuario_form.save(commit=False)
            usuario.personaId = persona
            usuario.reputacion = 0.0
            usuario.cant_valoraciones = 0
            usuario.save()
            return redirect('/')
        
        return render(request, "sesiones/signup.html", {
                'form_persona': persona_form,
                'form_usuario': usuario_form
            })
  
  
def list_users(request):
    usuarios = Usuario.objects.all()
    return render(request, "sesiones/listadoUsuarios.html", {
        'usuarios': usuarios
    })      


def edit_user(request, user_id):
    usuario = get_object_or_404(Usuario, pk=user_id)
    persona = get_object_or_404(Persona, pk=usuario.personaId.id)
    fecha_nac_formateada = usuario.fecha_nac.strftime('%d/%m/%Y')
    if request.method == "GET":
        formulario_usuario = EditarUsuarioForm(instance=usuario)
        formulario_persona = EditarPersonaForm(instance=persona)
    else:
        formulario_usuario_nuevo = EditarUsuarioForm(request.POST, instance=usuario)
        formulario_persona_nueva = EditarPersonaForm(request.POST, instance=persona)
        print(formulario_usuario_nuevo)
        if formulario_usuario_nuevo.is_valid() and formulario_persona_nueva.is_valid():
            print('es valido')
            formulario_persona_nueva.save()
            formulario_usuario_nuevo.save()
            return redirect('/')
        else:
            formulario_persona = formulario_persona_nueva
            formulario_usuario = formulario_usuario_nuevo
    return render(request, "sesiones/editUser.html", {
        'form_persona': formulario_persona,
        'form_usuario': formulario_usuario,
        'fecha_nac': fecha_nac_formateada
    })


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

    
def delete(request):
    if request.method == "GET":
        Usuario.objects.all().delete()
    return redirect("/")

def delete_user(request, user_id):
    usuario = get_object_or_404(Usuario, pk=user_id)
    if request.method == "POST":
        usuario.delete()
        return redirect('sesiones:list_users')
    return render(request, 'sesiones/deleteUser.html', { 'usuario': usuario })

    
def list_helpers(request):
    ayudantes = Ayudante.objects.exclude(nombre_usuario='eliminado')
    return render(request, "listadoAyudantes.html", {
        'ayudantes': ayudantes
    })   

def edit_intern(request, helper_id):
    ayudante = get_object_or_404(Ayudante, pk=helper_id)
    persona = get_object_or_404(Persona, pk=ayudante.personaId.id)
    ayudante_form = EditarAyudanteForm(instance=ayudante)
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

    return render(request, 'edit_intern.html', {'formPerson': persona_form, 'formAyudante': ayudante_form})