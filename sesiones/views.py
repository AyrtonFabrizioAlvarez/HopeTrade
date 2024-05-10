from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from sesiones.models import Persona, Usuario, Ayudante
from datetime import date
from django.shortcuts import get_object_or_404
from .forms import RegistroUsuario, EditarUsuario, EditarPersona
from .forms import IniciarSesionUsuario
from .models import Usuario, Persona
from .forms import RegistroUsuario, RegistroAyudante, ModificarInterno
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from hopetrade import settings

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
def signup_user(request):
    return HttpResponse("se creo el usuario")


def signup_helper(request):
    if request.method == "GET":
        return render(request, "signup_helper.html", {
            'form': RegistroAyudante()
        })
    else:
        persona = Persona.objects.create(nombre=request.POST['nombre'], apellido=request.POST['apellido'], contraseña=request.POST['contraseña'])
        persona.save()
        ayudante = Ayudante.objects.create(nombre_usuario=request.POST['nombre_usuario'], personaId=persona)
        ayudante.save()
        return redirect('/')

def edit_intern(request, helper_id):
    if request.method == "GET":
        intern = get_object_or_404(Ayudante, pk=helper_id)
        return render(request, "edit_intern.html", {
            'form': ModificarInterno()
        })
    else:
        persona = Persona.objects.create(nombre=request.POST['nombre'], apellido=request.POST['apellido'], contraseña=request.POST['contraseña'])
        persona.save()
        ayudante = Ayudante.objects.create(nombre_usuario=request.POST['nombre_usuario'], personaId=persona)
        ayudante.save()
        return redirect('/')

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

