from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from sesiones.models import Persona, Usuario, Ayudante
from django.shortcuts import get_object_or_404
from .forms import IniciarSesionUsuario, RecuperarClave
from .forms import PersonaForm, UsuarioForm, AyudanteForm, EditarUsuarioForm, EditarPersonaForm, EditarAyudanteForm
from .models import Persona, Usuario, Ayudante
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from hopetrade import settings

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


def enviar_mail(subject, message, to_email, nombre):
    name = nombre
    mail = to_email
    subject = subject
    message = message 

    template = render_to_string("email_template.html", {
        "name": name,
        "email": mail,
        "message": message
    })

    email = EmailMessage(
        subject,
        template,
        settings.EMAIL_HOST_USER,
        [mail]
    )

    email.fail_silently = False
    email.content_subtype = "html"
    email.send(fail_silently = False)


def signin(request):
    if request.method == "GET":
        return render(request, "signin.html", {"form": IniciarSesionUsuario()})
    elif request.method == "POST":
        action = request.POST.get("action")
        if action == "getpass":
            # Si la acción es "getpass", redirige a la página de recuperación de contraseña
            return redirect("signin/recuperarclave/")
        else:
            form = IniciarSesionUsuario(request.POST)
            if form.is_valid():
                dnii = form.cleaned_data.get('dni')
                password = form.cleaned_data.get('contraseña')
                try:
                    user = Usuario.objects.get(dni=dnii)
                    persona = user.personaId

                    # Verificar que el usuario no este bloqueado
                    if persona.intentos < 3:
                        # Verificar la contraseña del usuario
                        if user.personaId.contraseña == password:
                            # Iniciar sesión
                            request.session['usuario_id'] = user.id
                            persona.intentos = 0
                            persona.save()
                            return redirect("/")  # Redirigir a la página principal después del login
                        else:
                            # Contraseña incorrecta

                            # Aumento la cantidad de intentos
                            persona.intentos = persona.intentos + 1
                            persona.save()
                            if persona.intentos == 3:
                                error = "El usuario y/o contraseña ingresados son incorrectos. Su cuenta ha sido bloqueada"
                                enviar_mail("Bloqueo de cuenta", "Tu cuenta ha sido bloqueada", user.email, persona.nombre)
                            else:
                                error = "El usuario y/o contraseña ingresados son incorrectos."
                            return render(request, "signin.html", {"form": form, "error": error})
                    else:
                        error = "El usuario con el que desea ingresar se encuentra bloqueado"
                        return render(request, "signin.html", {"form": form, "error": error})
                    
                except Usuario.DoesNotExist:
                    # Usuario no encontrado
                    error = "El usuario y/o contraseña ingresados son incorrectos."
                    return render(request, "signin.html", {"form": form, "error": error})
            else:
                # Formulario no válido
                return render(request, "signin.html", {"form": form})  

def signout(request):
    if request.method == "GET":
        return render(request, "signout.html")
    elif request.method == "POST":
        action = request.POST.get("action")
        if action == "confirm":
            request.session['usuario_id'] = -1
            print(request.session['usuario_id'])
            return redirect("/")
        elif action == "cancel":
            return redirect("/")

def recuperar_contrasenia(request):
    if request.method == "GET":
        return render(request, "recuperarClave.html", {"form": RecuperarClave()})
    elif request.method == "POST":
        form = RecuperarClave(request.POST)
        if form.is_valid():
            dnii = form.cleaned_data.get('dni')
            try:
                user = Usuario.objects.get(dni=dnii)
                persona = user.personaId
                contrasenia = persona.contraseña
                subject = f"¡Hola!, tu contraseña para poder ingresar a Hope Trade es {contrasenia}"
                enviar_mail("Tu contraseña de Hope Trade", subject, user.email, persona.nombre)
                return render(request, "recuperarClave.html", {"form": RecuperarClave()})
            except Usuario.DoesNotExist:
                error = "El usuario ingresado no existe en el sistema"
                return render(request, "recuperarClave.html", {"form": RecuperarClave(), "error": error})
        else:
            # Formulario no válido
            return render(request, "signin.html", {"form": form})  