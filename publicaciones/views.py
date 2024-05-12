from django.shortcuts import render, redirect
from publicaciones.models import Publicacion
from publicaciones.models import Comentario
from sesiones.models import Usuario
from .forms import RealizarPublicacion
from .forms import RealizarComentario
from datetime import datetime   

# Create your views here.
def realizar_publicacion(request):
    if request.method == "POST":    
        realizar_publicacion_form = RealizarPublicacion(request.POST, request.FILES)
        if realizar_publicacion_form.is_valid():
            try:
                publicacion = realizar_publicacion_form.save(commit=False)
                publicacion.usuarioId = Usuario.objects.get(id=77) #hay que modificar el user
                if Publicacion.objects.filter(titulo=publicacion.titulo, usuarioId=publicacion.usuarioId).exists():
                    return render(request, "publicaciones/realizar_publicacion.html", {
                    'form': RealizarPublicacion(),
                    "error": 'No se pudo realizar la publicación, actualmente ya posee una publicación con el mismo título'
                })  
                publicacion.categoria_id = realizar_publicacion_form.cleaned_data['categoriaId'].id
                publicacion.aceptada = False
                publicacion.save()
                return redirect('/')
            except:
                return render(request, "publicaciones/realizar_publicacion.html", {
                    'form': RealizarPublicacion(),
                    "error": 'algo salió mal'
                })  
    else:
        realizar_publicacion_form = RealizarPublicacion()
    return render(request, "publicaciones/realizar_publicacion.html", {
        'form': RealizarPublicacion()
    })

def cancelar_operacion(request):
    return redirect('/')

def realizar_comentario(request, publicacion_id):
    if request.method == "POST":
        realizar_comentario_form = RealizarComentario(request.POST)
        if realizar_comentario_form.is_valid():
            try:
                comentario = realizar_comentario_form.save(commit=False)
                comentario.fecha = datetime.now()
                comentario.usuarioId = Usuario.objects.get(id=1)
                comentario.publicacionId = Publicacion.objects.get(id=publicacion_id) #falla aca
                comentario.save()
                return redirect('publicaciones/seleccionar_publicacion', publicacion_id=publicacion_id)
            except:
                return render(request, "publicaciones/realizar_comentario.html", {
                    'form': RealizarComentario(),
                    "error": 'algo salió mal'
                })
    return render(request, "publicaciones/realizar_comentario.html", {
        'form': RealizarComentario()
    })

def listar_publicaciones_sistema(request):
    publicacionesSistema = Publicacion.objects.all()
    if not publicacionesSistema:
        mensaje = "No existen publicaciones activas en este momento"
    else :
        mensaje = None
    return render(request, "publicaciones/listar_publicaciones_sistema.html", {
        'publicacionesSistema': publicacionesSistema
    })  


def listar_publicaciones_usuario(request):
    usuario = Usuario.objects.get(id=1)
    publicacionesUsuario = Publicacion.objects.filter(usuarioId=usuario)
    if not publicacionesUsuario:
        mensaje = "No existen publicaciones activas en este momento"
    else :
        mensaje = None
    return render(request, "publicaciones/listar_publicaciones_usuario.html", {
        'publicacionesUsuario': publicacionesUsuario
    })  

def seleccionar_publicacion(request, publicacion_id):
    publicacion = Publicacion.objects.get(id=publicacion_id)
    comentarios = Comentario.objects.filter(publicacionId=publicacion_id)
    return render(request, 'publicaciones/seleccionar_publicacion.html', {'publicacion': publicacion, 'comentarios': comentarios})