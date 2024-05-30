from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from sesiones.models import Persona, Usuario, Ayudante
from django.shortcuts import get_object_or_404
from .forms import IniciarSesionUsuario, RecuperarClave
from .forms import PersonaForm, UsuarioForm, AyudanteForm, EditarUsuarioForm, EditarPersonaForm, EditarAyudanteForm
from .models import Persona, Usuario, Ayudante, Administrador
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib import messages
from hopetrade import settings
import random
import string

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
        persona_form = PersonaForm(request.POST)
        usuario_form = UsuarioForm(request.POST)
        print(persona_form.is_valid())
        print(usuario_form.is_valid())
        if persona_form.is_valid() and usuario_form.is_valid():
            persona = persona_form.save(commit=False)
            persona.intentos = 0
            persona.rol = 'usuario'
            persona.save()
            usuario = usuario_form.save(commit=False)
            usuario.personaId = persona
            usuario.reputacion = 0.0
            usuario.cant_valoraciones = 0
            usuario.save()
            messages.success(request, "El usuario se creó exitosamente")
            return redirect('/')
        
        return render(request, "sesiones/signup.html", {
                'form_persona': persona_form,
                'form_usuario': usuario_form
            })
  
  
def list_users(request):
    usuarios = Usuario.objects.exclude(email='eliminado')
    if len(usuarios) == 0:
        messages.warning(request, 'No existen usuarios en el sistema')
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
        if formulario_usuario_nuevo.is_valid() and formulario_persona_nueva.is_valid():
            formulario_persona_nueva.save()
            formulario_usuario_nuevo.save()
            request.session['nombre'] = request.POST['nombre']
            return redirect('/')
        else:
            formulario_persona = formulario_persona_nueva
            formulario_usuario = formulario_usuario_nuevo
    return render(request, "sesiones/editUser.html", {
        'form_persona': formulario_persona,
        'form_usuario': formulario_usuario,
        'fecha_nac': fecha_nac_formateada
    })
    
def view_profile_user(request, user_id):
    usuario = get_object_or_404(Usuario, pk=user_id)
    persona = get_object_or_404(Persona, pk=usuario.personaId.id)
    fecha_nac_formateada = usuario.fecha_nac.strftime('%d/%m/%Y')
    formulario_usuario = UsuarioForm(instance=usuario)
    formulario_persona = PersonaForm(instance=persona)
    return render(request, "sesiones/view_profile_user.html", {'form_persona': formulario_persona,'form_usuario': formulario_usuario,
    'fecha_nac': fecha_nac_formateada, 'id':user_id, 'persona_id':persona.id})
    
def view_profile_helper(request, helper_id):
    intern = get_object_or_404(Ayudante, pk=helper_id)
    persona = get_object_or_404(Persona, pk=intern.personaId.id)
    estandar_form = AyudanteForm(instance=intern)
    persona_form = PersonaForm(instance=persona)
    return render(request, 'sesiones/view_profile_intern.html', {'form_persona': persona_form, 'form_ayudante': estandar_form, 'id':helper_id})

def view_profile_admin(request, admin_id):
    intern = get_object_or_404(Administrador, pk=admin_id)
    persona = get_object_or_404(Persona, pk=intern.personaId.id)
    estandar_form = AyudanteForm(instance=intern)
    persona_form = PersonaForm(instance=persona)
    return render(request, 'sesiones/view_profile_admin.html', {'form_persona': persona_form, 'form_admin': estandar_form, 'id':admin_id})

def edit_admin(request, admin_id):
    intern = get_object_or_404(Administrador, pk=admin_id)
    persona = get_object_or_404(Persona, pk=intern.personaId.id)
    ayudante_form = EditarAyudanteForm(instance=intern)
    persona_form = EditarPersonaForm(instance=persona)
    if request.method == 'POST':
        nueva_persona_form = EditarPersonaForm(request.POST)
        if nueva_persona_form.is_valid():
            persona = persona_form.save(commit=False)
            persona.nombre = request.POST['nombre']
            persona.apellido = request.POST['apellido']
            persona.contraseña = request.POST['contraseña']
            request.session['nombre'] = persona.nombre
            persona.save()
            return redirect('/')
        else:
            persona_form = nueva_persona_form

    return render(request, 'sesiones/edit_admin.html', {'form_persona': persona_form, 'form_admin': ayudante_form})


def delete_helper(request, helper_id):
    ayudante = get_object_or_404(Ayudante, pk=helper_id)
    if request.method == "POST":
        ayudante.nombre_usuario = 'eliminado'
        ayudante.save()
        return redirect('sesiones:list_helpers')
    return render(request, 'sesiones/deleteHelper.html', { 'ayudante': ayudante })


def signup_helper(request):
    if request.method == 'POST':
        persona_form = PersonaForm(request.POST)
        ayudante_form = AyudanteForm(request.POST)
        if persona_form.is_valid() and ayudante_form.is_valid():
            persona = persona_form.save(commit=False)
            persona.rol = 'ayudante'
            persona.intentos = 0
            persona.save()
            ayudante = ayudante_form.save(commit=False)
            ayudante.personaId = persona
            ayudante.save()
            messages.success(request, "El ayudante se creó exitosamente")
            return redirect('/')
    else:
        persona_form = PersonaForm()
        ayudante_form = AyudanteForm()

    return render(request, 'sesiones/signup_helper.html', {'form_persona': persona_form, 'form_ayudante': ayudante_form})

    
def delete(request):
    if request.method == "GET":
        Usuario.objects.all().delete()
    return redirect("/")

def delete_user(request, user_id):
    usuario = get_object_or_404(Usuario, pk=user_id)
    if request.method == "POST":
        usuario.dni = 0
        usuario.email = 'eliminado'
        usuario.save()
        return redirect('sesiones:list_users')
    return render(request, 'sesiones/deleteUser.html', { 'usuario': usuario })

    
def list_helpers(request):
    ayudantes = Ayudante.objects.exclude(nombre_usuario='eliminado')
    if len(ayudantes) == 0:
        messages.warning(request, 'No existen ayudantes en el sistema')
    return render(request, "sesiones/listadoAyudantes.html", {
        'ayudantes': ayudantes
    })   

def edit_intern(request, helper_id):
    intern = get_object_or_404(Ayudante, pk=helper_id)
    persona = get_object_or_404(Persona, pk=intern.personaId.id)
    ayudante_form = EditarAyudanteForm(instance=intern)
    persona_form = EditarPersonaForm(instance=persona)
    if request.method == 'POST':
        nueva_persona_form = EditarPersonaForm(request.POST)
        if nueva_persona_form.is_valid():
            persona = persona_form.save(commit=False)
            persona.nombre = request.POST['nombre']
            persona.apellido = request.POST['apellido']
            persona.contraseña = request.POST['contraseña']
            request.session['nombre'] = persona.nombre
            persona.save()
            return redirect('/')
        else:
            persona_form = nueva_persona_form

    return render(request, 'sesiones/edit_intern.html', {'form_persona': persona_form, 'form_ayudante': ayudante_form})


def enviar_mail(subject, message, to_email, nombre):
    name = nombre
    mail = to_email
    subject = subject
    message = message 

    template = render_to_string("sesiones/email_template.html", {
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
        return render(request, "sesiones/signin.html", {"form": IniciarSesionUsuario()})
    elif request.method == "POST":
        action = request.POST.get("action")
        if action == "getpass":
            # Si la acción es "getpass", redirige a la página de recuperación de contraseña
            return redirect("/sesiones/recuperarclave.html")
        elif action == "signin":
            form = IniciarSesionUsuario(request.POST)
            if form.is_valid():
                clave = form.cleaned_data.get('usuario')
                password = form.cleaned_data.get('contraseña')

                # Compruebo si la clave es un dni o nombre de usuario
                if (clave.isdigit()):
                    return inicio_sesion_usuario(request, clave, password, form)
                else:
                    return inicio_sesion_interno(request, clave, password, form)

            else:
                # Formulario no válido
                return render(request, "sesiones/signin.html", {"form": form})  
               

def inicio_sesion_usuario(request, clave, password, form):
    try:
        user = Usuario.objects.get(dni=clave)
        persona = user.personaId

        # Verificar que el usuario no este bloqueado
        if persona.intentos < 3:
            # Verificar la contraseña del usuario
            if user.personaId.contraseña == password:
                # Iniciar sesión
                request.session['usuario_id'] = persona.id
                request.session['nombre'] = persona.nombre
                request.session['rol'] = 'usuario'
                request.session['rol_id'] = user.id
                print(request.session['usuario_id'])
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
                    enviar_mail("Bloqueo de cuenta", "Tu cuenta ha sido bloqueada, para desbloquearla ve al inicio de sesión, presione '¿Olvidaste tu contraseña?', ingrese su DNI, presiona 'Recuperar contraseña' y nosotros te enviaremos otro mail para recuperarla ", user.email, persona.nombre)
                else:
                    error = "El usuario y/o contraseña ingresados son incorrectos."
                return render(request, "sesiones/signin.html", {"form": form, "error": error})
        else:
            error = "El usuario con el que desea ingresar se encuentra bloqueado"
            return render(request, "sesiones/signin.html", {"form": form, "error": error})
        
    except Usuario.DoesNotExist:
        # Usuario no encontrado
        error = "El usuario y/o contraseña ingresados son incorrectos."
        return render(request, "sesiones/signin.html", {"form": form, "error": error})

def inicio_sesion_interno(request, clave, password, form):
    try:
        ayudante = Ayudante.objects.get(nombre_usuario=clave)
        persona = ayudante.personaId
        if persona.contraseña == password:
            request.session['usuario_id'] = persona.id
            request.session['nombre'] = persona.nombre
            request.session['rol'] = 'ayudante'
            request.session['rol_id'] = ayudante.id
            print(request.session['usuario_id'])
            return redirect("/")
        else:
            error = "El usuario y/o contraseña ingresados son incorrectos."
            return render(request, "sesiones/signin.html", {"form": form, "error": error})
        
    except Ayudante.DoesNotExist:
        # Usuario no encontrado
        try:
            admin = Administrador.objects.get(nombre_usuario=clave)
            persona = admin.personaId
            if persona.contraseña == password:
                # Iniciar sesión
                request.session['usuario_id'] = persona.id
                request.session['nombre'] = persona.nombre
                request.session['rol'] = 'administrador'
                request.session['rol_id'] = admin.id
                print(request.session['usuario_id'])
                return redirect("/")  
            else:
                error = "El usuario y/o contraseña ingresados son incorrectos."
                return render(request, "sesiones/signin.html", {"form": form, "error": error})
        except Administrador.DoesNotExist:
            error = "El usuario y/o contraseña ingresados son incorrectos."
            return render(request, "sesiones/signin.html", {"form": form, "error": error})
        
def signout(request):
    if request.method == "GET":
        return render(request, "sesiones/signout.html")
    elif request.method == "POST":
        action = request.POST.get("action")
        if action == "confirm":
            request.session.clear()
            
            persona_id = request.session.get('usuario_id', None)
            print(persona_id)
            
            return redirect("/")
        elif action == "cancel":
            return redirect("/")

def recuperar_contrasenia(request):
    if request.method == "GET":
        return render(request, "sesiones/recuperarClave.html", {"form": RecuperarClave()})
    elif request.method == "POST":
        form = RecuperarClave(request.POST)
        if form.is_valid():
            dnii = form.cleaned_data.get('dni')
            try:
                user = Usuario.objects.get(dni=dnii)
                persona = user.personaId
                if (persona.intentos == 3):
                    persona.contraseña = generate_otp(8)
                    persona.intentos = 0
                    persona.save()
                contrasenia = persona.contraseña
                subject = f"¡Hola!, tu contraseña para poder ingresar a Hope Trade es {contrasenia}"
                enviar_mail("Tu contraseña de Hope Trade", subject, user.email, persona.nombre)
                messages.success(request, 'Se le envió un email con su contraseña')
                return render(request, "sesiones/recuperarClave.html", {"form": RecuperarClave()})
            except Usuario.DoesNotExist:
                error = "El usuario ingresado no existe en el sistema"
                return render(request, "sesiones/recuperarClave.html", {"form": RecuperarClave(), "error": error})
        else:
            # Formulario no válido
            return render(request, "sesiones/signin.html", {"form": form})  

def generate_otp(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    otp = "".join(random.choice(characters) for _ in range(length))
    return otp

otp_code = generate_otp(10)